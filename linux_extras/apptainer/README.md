# Running eduActiv8 with Apptainer

This optional method allows you to run **eduActiv8** inside an [Apptainer](https://apptainer.org/) container, providing an easy way to deploy the application on different Linux distributions without worrying about package versions or dependencies.

The included `eduactiv8_fedora42.def` file can be used to build a self-contained Apptainer image based on Fedora 42.
File created by Paul Zakharov and original available at: [https://gist.github.com/paulz1/7871a00f043c6e76d347b2a0e5fc1d93](https://gist.github.com/paulz1/7871a00f043c6e76d347b2a0e5fc1d93)

## Prerequisites

You’ll need **Apptainer** installed on your system.
Please refer to the official installation guide for your distribution:
👉 [https://apptainer.org/docs/](https://apptainer.org/docs/)

No root (administrator) privileges are required to build or run the container in most cases.

## Building the Container

Once Apptainer is installed, simply run the following command in the same directory as the definition file:

```
apptainer build eduactiv8.sif eduactiv8_fedora42.def
```

This command will create a single file named `eduactiv8.sif`, which contains the complete runtime environment for eduActiv8.

## Running eduActiv8

After building the container, make it executable and run it:

```
chmod u+x eduactiv8.sif
./eduactiv8.sif
```

eduActiv8 should now start in its containerised environment.

## Advantages

* Works across various Linux distributions.
* Does not require admin privileges to run.
* Produces a portable `.sif` file that can easily be copied to other systems.

## Notes

This Apptainer-based method is **not the primary installation method** for eduActiv8, but rather an optional alternative for users who prefer containerised environments or encounter compatibility issues on older distributions.

For typical installations or packaging formats better suited to end users (e.g. AppImage), please refer to the main [eduActiv8 installation instructions](../../README.md).

