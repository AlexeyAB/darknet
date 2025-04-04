import sys
import os


def get_dataset_images_relative_paths(dataset_directory_name):
    """
    Gets list of paths to the dataset images.

    :param dataset_directory_name: dataset directory name
    :return: dataset images relative paths
    """
    os.chdir("..")
    os.chdir(os.path.join("data", dataset_directory_name))

    dataset_images_relative_paths = []
    for dataset_image_name in os.listdir(os.getcwd()):
        if dataset_image_name.endswith(".jpg"):
            dataset_images_relative_paths.append(f"data/{dataset_directory_name}/{dataset_image_name}")

    return dataset_images_relative_paths


def write_dataset_images_relative_paths(dataset_directory_name, dataset_images_relative_paths):
    """
    Writes dataset images relative paths

    :param dataset_directory_name: dataset directory name
    :param dataset_images_relative_paths: dataset images relative paths
    """
    os.chdir("..")

    with open(f"{dataset_directory_name}.txt", "w") as dataset_images_relative_paths_file:
        for dataset_image_relative_path in dataset_images_relative_paths:
            dataset_images_relative_paths_file.write(f"{dataset_image_relative_path}\n")


def main():
    """
    Script entry point.
    """
    # Check whether dataset directory name is not provided
    if len(sys.argv) != 2:
        sys.exit("You need to provide dataset directory name!")

    # Get dataset directory name
    dataset_directory_name = sys.argv[1]

    # Write dataset images relative paths
    write_dataset_images_relative_paths(dataset_directory_name,
                                        get_dataset_images_relative_paths(dataset_directory_name))


if __name__ == "__main__":
    main()
