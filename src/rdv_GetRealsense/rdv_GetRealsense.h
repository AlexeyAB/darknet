// include the librealsense C++ header file
#include <librealsense2/rs.hpp>

// include OpenCV header file
#include <opencv2/opencv.hpp>
#include <boost/thread.hpp>

#include <atomic>
#include <string>

struct filter_slider_ui
{
    std::string name;
    std::string label;
    std::string description;
    bool is_int;
    float value;
    rs2::option_range range;

    //bool render(const float3& location, bool enabled);
    static bool is_all_integers(const rs2::option_range& range);
};

/**
Class to encapsulate a filter alongside its options
*/
class filter_options 
{
public:
    filter_options(const std::string name, rs2::filter& filter);
    filter_options(filter_options&& other);
    std::string filter_name;                                   //Friendly name of the filter
    rs2::filter& filter;                                       //The filter in use
    std::map<rs2_option, filter_slider_ui> supported_options;  //maps from an option supported by the filter, to the corresponding slider
    std::atomic_bool is_enabled;                               //A boolean controlled by the user that determines whether to apply the filter or not
};

class CRealsense
{
public:
    CRealsense(void);
    ~CRealsense(void);

public :
	cv::Mat Get_Image_RGB(void) ;
	cv::Mat Get_Image_Depth(void) ;
	cv::Mat Get_Value_Depth(void) ;
	cv::Mat Get_Image_Colormap(void) ;

	cv::Mat Get_Value_Depth2(void) ;
	
private:
	//Network Thread
	//thread
	bool m_run_thread;			//boost thread exit value
	boost::thread m_thread;		//network thread
	boost::mutex m_mutex;
	void ThreadFunction(void) ;
	
	rs2::pipeline m_pipe;
	rs2::config m_cfg;

	cv::Mat m_mat_color ;
	cv::Mat m_mat_depth ;
	cv::Mat m_mat_depth_color ;
	cv::Mat m_mat_filtered ;

	cv::Mat m_mat_cloud ;
	cv::Mat Points_to_Mat(const rs2::points& points) ;
	
};


