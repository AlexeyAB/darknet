package dark;

import com.sun.jna.Pointer;
import com.sun.jna.Structure;
import com.sun.jna.ptr.PointerByReference;

public class tree extends Structure {
        Pointer leaf;
        int n;
        Pointer parent;
        Pointer child;
        Pointer group;
        PointerByReference name;
        int groups;
        Pointer group_size;
        Pointer group_offset;
}

/*

// tree.h
typedef struct tree {
    int *leaf;
    int n;
    int *parent;
    int *child;
    int *group;
    char **name;

    int groups;
    int *group_size;
    int *group_offset;
} tree;

 */
