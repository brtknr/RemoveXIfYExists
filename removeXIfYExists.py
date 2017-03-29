#!/usr/bin/python
import os

# define your file extensions here, case is ignored.
# Please start with a dot.
# multiple Y extensions allowed, single X extension only
Y_extensions = (".dng", ".cR2", ".nef", ".crw")
X_extension = ".jpg"

# Change this to True if you want to remove the Xs for real
remove_for_real = True

# define waste basket directory here. Include trainling slash or backslash.
# Windows : waste_dir = "C:\path\to\waste\" 
waste_dir = "./waste" 

##### do not modify below ##########

# find files 
def locate(folder, extensions):
    '''Locate files in directory with given extensions'''
    for filename in os.listdir(folder):
        if filename.endswith(extensions):
            yield os.path.join(folder, filename) 

# make waste basket dir
if not os.path.exists(waste_dir):
    os.makedirs(waste_dir)

# Make search case insensitive    
Y_ext = tuple(map(str.lower,Y_extensions)) + tuple(map(str.upper,Y_extensions))
X_ext = (X_extension.lower(), X_extension.upper())

root=os.curdir
#find subdirectories
for path, dirs, files in os.walk(os.path.abspath(root)):
    print path
    Y_hash = {}
    for Y in locate(path, Y_ext):
        base_name = os.path.basename(Y)
        base_name = os.path.splitext(base_name)[0]
        Y_hash[base_name] = True

    # find pairs and move Xs of pairs to waste basket    
    for X in locate(path, X_ext):
        base_name = os.path.basename(X)
        base_name = os.path.splitext(base_name)[0]
        if base_name in Y_hash:
            X_base_name_with_ext = base_name + X_extension
            new_X_dir = waste_dir + path + '/'
            if not os.path.exists(new_X_dir):
                os.makedirs(new_X_dir)            
            new_X = new_X_dir + X_base_name_with_ext
            print ("{}: {} = {} => {}".format(path, base_name, X, waste_dir))
            if os.path.exists(new_X):
                if remove_for_real:
                    os.remove(X)
            else:
                os.rename(X, new_X)