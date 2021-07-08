using System;
using System.Runtime.InteropServices;

namespace Darknet
{
    public class YoloWrapper : IDisposable
    {
        private const string YoloLibraryName = "yolo_cpp_dll.dll";
        private const int MaxObjects = 1000;

        [DllImport(YoloLibraryName, EntryPoint = "init")]
        private static extern IntPtr InitializeYolo(string configurationFilename, string weightsFilename, int gpu);

        [DllImport(YoloLibraryName, EntryPoint = "detect_image")]
        private static extern int DetectImage(IntPtr pDetector, string filename, float threshold, ref BboxContainer container);

        [DllImport(YoloLibraryName, EntryPoint = "detect_mat")]
        private static extern int DetectImage(IntPtr pDetector, IntPtr pArray, int nSize, float threshold, ref BboxContainer container);

        [DllImport(YoloLibraryName, EntryPoint = "get_net_width")]
        private static extern int LibGetNetWidth(IntPtr pDetector);

        [DllImport(YoloLibraryName, EntryPoint = "get_net_height")]
        private static extern int LibGetNetHeight(IntPtr pDetector);

        [DllImport(YoloLibraryName, EntryPoint = "get_net_color_depth")]
        private static extern int LibGetNetColorDepth(IntPtr pDetector);

        [DllImport(YoloLibraryName, EntryPoint = "dispose")]
        private static extern void DisposeYolo(IntPtr pDetector);

        [StructLayout(LayoutKind.Sequential)]
        public struct bbox_t
        {
            public UInt32 x, y, w, h;    // (x,y) - top-left corner, (w, h) - width & height of bounded box
            public float prob;           // confidence - probability that the object was found correctly
            public UInt32 obj_id;        // class of object - from range [0, classes-1]
            public UInt32 track_id;      // tracking id for video (0 - untracked, 1 - inf - tracked object)
            public UInt32 frames_counter;
            public float x_3d, y_3d, z_3d;  // 3-D coordinates, if there is used 3D-stereo camera
        };

        [StructLayout(LayoutKind.Sequential)]
        public struct BboxContainer
        {
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = MaxObjects)]
            public bbox_t[] candidates;
        }

        private IntPtr pDetector;

        public YoloWrapper(string configurationFilename, string weightsFilename, int gpu)
        {
            pDetector = InitializeYolo(configurationFilename, weightsFilename, gpu);
        }

        public void Dispose()
        {
            if (pDetector != IntPtr.Zero)
            {
                DisposeYolo(pDetector);
                pDetector = IntPtr.Zero;
            }
        }

        public int NetworkWidth => LibGetNetWidth(pDetector);

        public int NetworkHeight => LibGetNetHeight(pDetector);

        public int NetworkColorDepth => LibGetNetColorDepth(pDetector);

        public bbox_t[] Detect(string filename, float threshold = 0.2f)
        {
            var container = new BboxContainer();
            var count = DetectImage(pDetector, filename, threshold, ref container);

            return container.candidates;
        }

        public bbox_t[] Detect(byte[] imageData, float threshold = 0.2f)
        {
            var container = new BboxContainer();

            var size = Marshal.SizeOf(imageData[0]) * imageData.Length;
            var pnt = Marshal.AllocHGlobal(size);

            try
            {
                // Copy the array to unmanaged memory.
                Marshal.Copy(imageData, 0, pnt, imageData.Length);
                var count = DetectImage(pDetector, pnt, imageData.Length, threshold, ref container);
                if (count == -1)
                {
                    throw new NotSupportedException($"{YoloLibraryName} has no OpenCV support");
                }
            }
            catch (Exception exception)
            {
                return null;
            }
            finally
            {
                // Free the unmanaged memory.
                Marshal.FreeHGlobal(pnt);
            }

            return container.candidates;
        }
    }
}
