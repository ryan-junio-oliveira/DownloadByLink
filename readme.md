```
pyinstaller --onefile --windowed --add-data "./azure.tcl;./theme." --distpath ./ app.py #windows
pyinstaller --onefile --windowed --add-data "./azure.tcl:./theme." --distpath ./ app.py #linux/mac

```