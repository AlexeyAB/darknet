#include "rdv_GetRealsense.h"

CRealsense::CRealsense(void) 
{	
	//Start Network Accept Thread
	m_run_thread = true;
	m_thread = boost::thread(boost::bind(&CRealsense::ThreadFunction, this));
}

CRealsense::~CRealsense(void)
{
	m_run_thread = false ;
	m_thread.join() ;
}

void CRealsense::ThreadFunction(void)
{
	printf("CRealsense : 1\n") ;
	
	const int width = 640 ;
	const int height = 480 ;
	
	//Add desired streams to configuration
    m_cfg.enable_stream(RS2_STREAM_COLOR, width, height, RS2_FORMAT_BGR8, 30);
	m_cfg.enable_stream(RS2_STREAM_DEPTH, width, height, RS2_FORMAT_Z16, 30);
	//m_cfg.enable_stream(RS2_STREAM_DEPTH);
    //m_cfg.enable_stream(RS2_STREAM_COLOR);

	printf("CRealsense : 1-1\n") ;
	
	//Instruct pipeline to start streaming with the requested configuration
    m_pipe.start(m_cfg);

	
	// Define two align objects. One will be used to align
	// to depth viewport and the other to color.
	// Creating align object is an expensive operation
	// that should not be performed in the main loop
	rs2::align align_to_depth(RS2_STREAM_DEPTH);
	rs2::align align_to_color(RS2_STREAM_COLOR);

	printf("CRealsense : 2\n") ;
	
	// Camera warmup - dropping several first frames to let auto-exposure stabilize
    rs2::frameset frames;
    for(int i = 0; i < 30; i++)
    {
        //Wait for all configured streams to produce a frame
        frames = m_pipe.wait_for_frames();
    }

	printf("CRealsense : 3\n") ;

	// Declare filters
    rs2::decimation_filter dec_filter;  // Decimation - reduces depth frame density
    rs2::threshold_filter thr_filter;   // Threshold  - removes values outside recommended range
    rs2::spatial_filter spat_filter;    // Spatial    - edge-preserving spatial smoothing
    rs2::temporal_filter temp_filter;   // Temporal   - reduces temporal noise

                                        // Declare disparity transform from depth to disparity and vice versa
    const std::string disparity_filter_name = "Disparity";
    rs2::disparity_transform depth_to_disparity(true);
    rs2::disparity_transform disparity_to_depth(false);

    // Initialize a vector that holds filters and their options
    std::vector<filter_options> filters;

    // The following order of emplacement will dictate the orders in which filters are applied
    filters.emplace_back("Decimate", dec_filter);
    filters.emplace_back("Threshold", thr_filter);
    filters.emplace_back(disparity_filter_name, depth_to_disparity);
    filters.emplace_back("Spatial", spat_filter);
    filters.emplace_back("Temporal", temp_filter);

	//rs2::colorizer color_map; 
	printf("CRealsense : 4\n") ;
	//rs2::colorizer color_map;
	rs2::colorizer color_filter;	// Colorize - convert from depth to RGB color

	// Declare pointcloud object, for calculating pointclouds and texture mappings
    rs2::pointcloud pc;
    // We want the points object to be persistent so we can display the last cloud when a frame drops
    rs2::points points;
	
	while(m_run_thread)
	{
		frames = m_pipe.wait_for_frames();
		
	    //Get each frame
	    rs2::frame color_frame = frames.get_color_frame();
		//rs2::frame ir_frame = frames.first(RS2_STREAM_INFRARED);

		// Align
        frames = align_to_color.process(frames);
		
		rs2::frame depth_frame = frames.get_depth_frame();
		rs2::frame depth_frame_color = color_filter.process(depth_frame);
		
		
		//rs2::frame depth_color_frame = color_map(depth_frame); // Find and colorize the depth data
		//rs2::frame depth_frame = frames.first(RS2_STREAM_DEPTH, RS2_FORMAT_RGB8);
#if 0		
		rs2::frame filtered = depth_frame; // Does not copy the frame, only adds a reference

        /* Apply filters.
        The implemented flow of the filters pipeline is in the following order:
        1. apply decimation filter
        2. apply threshold filter
        3. transform the scene into disparity domain
        4. apply spatial filter
        5. apply temporal filter
        6. revert the results back (if step Disparity filter was applied
        to depth domain (each post processing block is optional and can be applied independantly).
        */
        bool revert_disparity = false;
        for (auto&& filter : filters)
        {
            if (filter.is_enabled)
            {
                filtered = filter.filter.process(filtered);
                if (filter.filter_name == disparity_filter_name)
                {
                    revert_disparity = true;
                }
            }
        }
        if (revert_disparity)
        {
            filtered = disparity_to_depth.process(filtered);
        }
#endif

		m_mutex.lock() ;
		
		// Creating OpenCV Matrix from a color image
		//if( m_mat_color.empty() )	m_mat_color = cv::Mat(cv::Size(width, height), CV_8UC3, (void*)color_frame.get_data(), cv::Mat::AUTO_STEP);
		cv::Mat mat_color = cv::Mat(cv::Size(width, height), CV_8UC3, (void*)color_frame.get_data(), cv::Mat::AUTO_STEP);
		mat_color.copyTo(m_mat_color) ;
		
		// Creating OpenCV matrix from IR image
	    //if( m_mat_depth.empty() ) m_mat_depth = cv::Mat(cv::Size(width, height), CV_16UC1, (void*)depth_frame.get_data(), cv::Mat::AUTO_STEP);
	    //cv::Mat mat_depth = cv::Mat(cv::Size(width, height), CV_16UC1, (void*)depth_frame.get_data(), cv::Mat::AUTO_STEP);
	    cv::Mat mat_depth_color = cv::Mat(cv::Size(width, height), CV_8UC3, (void*)depth_frame_color.get_data(), cv::Mat::AUTO_STEP);
		mat_depth_color.copyTo(m_mat_depth_color) ;

		cv::Mat mat_depth = cv::Mat(cv::Size(width, height), CV_16UC1, (void*)depth_frame.get_data(), cv::Mat::AUTO_STEP);
		mat_depth.copyTo(m_mat_depth) ;
		//Mat ir(Size(640, 480), CV_8UC1, (void*)ir_frame.get_data(), Mat::AUTO_STEP);

		//pcl point cloud
		// Generate the pointcloud and texture mappings
	    points = pc.calculate(depth_frame);
    	//m_p_cloud = points_to_pcl(points);
    	m_mat_cloud = Points_to_Mat(points);
		

#if 0
		// Creating OpenCV matrix from IR image
		// Query frame size (width and height)
        const int w = filtered.as<rs2::video_frame>().get_width();
        const int h = filtered.as<rs2::video_frame>().get_height();

		if( m_mat_filtered.empty() )	m_mat_filtered = cv::Mat(cv::Size(w, h), CV_16UC1, (void*)filtered.get_data(), cv::Mat::AUTO_STEP);
#endif		
		// Convert 16bit image to 8bit image
		//m_mat_depth.convertTo(m_mat_depth, CV_8UC1, 15 / 256.0);
		//m_mat_filtered.convertTo(m_mat_filtered, CV_8UC1, 15 / 256.0);

#if 0	
		cv::Mat display_depth ;
		m_mat_depth.convertTo(display_depth, CV_8UC1, 15 / 256.0);
		cv::Mat display_filtered ;
		m_mat_filtered.convertTo(display_filtered, CV_8UC1, 15 / 256.0);
		
		// Display in a GUI
		cv::imshow("Display Image", m_mat_color);
		cv::imshow("Depth Image", display_depth);
		cv::imshow("Filtered Image", display_filtered);
		//imshow("IR Image", ir);

		char c = cv::waitKey(1);

		//if( c == 'q' || c == 'Q' ) break ;
#endif

		m_mutex.unlock() ;

		boost::this_thread::sleep(boost::posix_time::millisec(1));
		boost::thread::yield() ;
	};

	m_pipe.stop() ;
}

cv::Mat CRealsense::Points_to_Mat(const rs2::points& points)
{
	auto sp = points.get_profile().as<rs2::video_stream_profile>();

	const int sp_width = sp.width();
	const int sp_height = sp.height();
	const int sp_size = points.size();

	printf("Points_to_Mat : w(%d), h(%d), s(%d)\n", sp_width, sp_height, sp_size) ;

	if( (m_mat_cloud.cols != sp_width || m_mat_cloud.rows != sp_height) && !m_mat_cloud.empty() )
	{
		m_mat_cloud.release() ;
	}

	if( m_mat_cloud.empty() )	m_mat_cloud = cv::Mat(cv::Size(sp_width, sp_height), CV_16UC1) ;

	unsigned short* ptr_cloud_data = (unsigned short*)m_mat_cloud.data; // v+1행 첫 칸의 주소를 불러온다. 

	auto ptr_s = points.get_vertices();
	int y_index = 0 ;
	for(int y= 0;y<m_mat_cloud.rows ; y++)
	{
		y_index = y * m_mat_cloud.cols ;
		
		for(int x = 0 ; x<m_mat_cloud.cols ; x++)
		{
			int index = y_index + x ;
			
			auto ptr = ptr_s + index ;
			
			ptr_cloud_data[y_index + x] = ptr->z; ; // v+1행 u+1열에 대한 연산을 수행한다. 
			
		}
	}

	return m_mat_cloud ;

#if 0	
	if( m_p_cloud == NULL )
	{
		m_p_cloud = new pcl::PointCloud<pcl::PointXYZ> ;
	}
	
    m_p_cloud->width = sp.width();
    m_p_cloud->height = sp.height();
    m_p_cloud->is_dense = false;
    m_p_cloud->points.resize(points.size());
    auto ptr = points.get_vertices();
    for (auto& p : m_p_cloud->points)
    {
        p.x = ptr->x;
        p.y = ptr->y;
        p.z = ptr->z;
        ptr++;
    }

    return m_p_cloud;
#endif	
}

cv::Mat CRealsense::Get_Image_RGB(void)
{
	cv::Mat ret_mat ;
	
	m_mutex.lock() ;
	m_mat_color.copyTo(ret_mat) ;
	m_mutex.unlock() ;

	return ret_mat ;
}

cv::Mat CRealsense::Get_Image_Depth(void)
{
	cv::Mat ret_mat ;
	
	m_mutex.lock() ;
	m_mat_depth_color.copyTo(ret_mat) ;
	//ret_mat.convertTo(ret_mat, CV_8UC1, 15 / 256.0);
	m_mutex.unlock() ;

	return ret_mat ;
}

cv::Mat CRealsense::Get_Value_Depth(void)
{
	cv::Mat ret_mat ;
	
	m_mutex.lock() ;
	m_mat_depth.copyTo(ret_mat) ;
	m_mutex.unlock() ;

	return ret_mat ;
}

cv::Mat CRealsense::Get_Value_Depth2(void)
{
	return m_mat_cloud ;
}

cv::Mat CRealsense::Get_Image_Colormap(void)
{
	return cv::Mat();
}

/**
Constructor for filter_options, takes a name and a filter.
*/
filter_options::filter_options(const std::string name, rs2::filter& flt) :
    filter_name(name),
    filter(flt),
    is_enabled(true)
{
    const std::array<rs2_option, 5> possible_filter_options = {
        RS2_OPTION_FILTER_MAGNITUDE,
        RS2_OPTION_FILTER_SMOOTH_ALPHA,
        RS2_OPTION_MIN_DISTANCE,
        RS2_OPTION_MAX_DISTANCE,
        RS2_OPTION_FILTER_SMOOTH_DELTA
    };

    //Go over each filter option and create a slider for it
    for (rs2_option opt : possible_filter_options)
    {
        if (flt.supports(opt))
        {
            rs2::option_range range = flt.get_option_range(opt);
            supported_options[opt].range = range;
            supported_options[opt].value = range.def;
            supported_options[opt].is_int = filter_slider_ui::is_all_integers(range);
            supported_options[opt].description = flt.get_option_description(opt);
            std::string opt_name = flt.get_option_name(opt);
            supported_options[opt].name = name + "_" + opt_name;
            std::string prefix = "Filter ";
            supported_options[opt].label = opt_name;
        }
    }
}

filter_options::filter_options(filter_options&& other) :
    filter_name(std::move(other.filter_name)),
    filter(other.filter),
    supported_options(std::move(other.supported_options)),
    is_enabled(other.is_enabled.load())
{
}

/**
  Helper function for deciding on int ot float slider
*/
bool filter_slider_ui::is_all_integers(const rs2::option_range& range)
{
    const auto is_integer = [](float f)
    {
        return (fabs(fmod(f, 1)) < std::numeric_limits<float>::min());
    };

    return is_integer(range.min) && is_integer(range.max) &&
        is_integer(range.def) && is_integer(range.step);
}

