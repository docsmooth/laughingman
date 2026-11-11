This directory contains the code for the LaughingMan watch face.

You must configure a watch before you can compile this code!

Run the Python 3 script config_watch.py in the root directory to configure the watch. You must have Python 3 and the Pillow imaging library (PIL) installed to run this script successfully. Use the command-line option -h to list the available options.

Once the watch is configured, the script writes package.json and src/pkjs/index.js, and you may use the pebble tool (RePebble SDK, run from WSL or Linux) to build it in the normal Pebble way.
