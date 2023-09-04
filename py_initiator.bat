::Create all applicable folders
if not exist py mkdir py
if not exist py\core mkdir py\core
if not exist py\libs mkdir py\libs 
if not exist py\data mkdir py\data

::Copying all the py content to debug and release folders
robocopy py bin\Debug\py /MIR
robocopy py bin\Release\py /MIR

pause
