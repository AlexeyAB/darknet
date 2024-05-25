package dark;

import org.bytedeco.javacpp.*;
import org.bytedeco.javacpp.annotation.*;
import org.bytedeco.javacpp.tools.*;


@Properties(
        value = @Platform(
                includepath = {"../../../../include/"},
                preloadpath = {"../../../.."},
                linkpath = {"../../../.."},
                include = {"darknet.h","yolo_v2_class.hpp"},
                //preload = {"DependentLib"},
                link = {"C:/wrk/darknet/dark.dll"}
        ),
        target = "dark.DarknetLibrary"
)

public class DarknetLibraryConfig implements InfoMapper {
    public void map(InfoMap infoMap) {
        //infoMap.put(new Info("darknet.h").linePatterns("#ifdef CUDNN", "#endif  // CUDNN").skip());
        //infoMap.put(new Info("darknet.h").linePatterns("#if defined(TRACK_OPTFLOW)", "#elif defined(TRACK_OPTFLOW)").skip());


    }
}

