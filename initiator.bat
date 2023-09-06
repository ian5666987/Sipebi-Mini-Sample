::Create all applicable folders
if not exist py mkdir py
if not exist py\core mkdir py\core
if not exist py\libs mkdir py\libs 
if not exist py\data mkdir py\data
if not exist bin\Debug mkdir bin\Debug
if not exist bin\Release mkdir bin\Release
if not exist Files mkdir Files

::Copying all the py content to debug and release folders
robocopy Files bin\Debug *.*
robocopy Files bin\Release *.*
robocopy py bin\Debug\py /MIR
robocopy py bin\Release\py /MIR

pause
