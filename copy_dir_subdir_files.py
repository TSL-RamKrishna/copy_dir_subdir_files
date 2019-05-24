#!/usr/bin/env python

import os, re, sys
import shutil
import argparse

# This python script copies dir/subdir/files to another file path with similar directory structure as in the original file path
# with the option --ext, only the files with selected extension will be copied.
# usage: python copy_dir_subdir_files.py --target target_dir --destination destination_dir --ext txt

Description="Program to copy the diretories, sub-directories and files of defined extensions"

usage="""
python ${script} --target /path/to/target/folder --destination /path/to/destination --ext comma-separated-file-extensions
""".format(script=sys.argv[0])


parser=argparse.ArgumentParser(description=Description, version="version 1.0", epilog=usage)

parser.add_argument("-t", "--target", action="store", dest="target", help="Provide the target folder to be copied")
parser.add_argument("-d", "--destination", action="store", dest="destination", help="Provide the destination folder where the directories, sub-directories and files will be copied")
parser.add_argument("-e", "--ext", action="store", dest="ext", help="Provide the comma separated list of file extensions, other file with extension not listed will be not be copied")
parser.add_argument("-l","--link", action="store_true", default=False, dest="link", help="create soft link instead of copying the files.")

options=parser.parse_args()

if not options.destination:
        print("Destination path not provided. By default, the current folder will be used as destination folder")
        options.destionation=os.getcwd()
else:
        options.destination=os.path.abspath(options.destination)

if not options.target:
        print("Target path is not provided")
        exit(1)
else:
        target_dirname=os.path.dirname(os.path.abspath(options.target))

if options.ext:
        old_list=options.ext.split(",")
        ext_list=[]
        for each in old_list:
                if each == '':
                        continue
                else:
                        ext_list.append(each)
        if len(ext_list)==0:
                print "It looks like you have not provided the extensions list or you provided blank extensions"
                exit(1)

else:
        print("Extension list not provided")
        exit(1)

if not os.path.exists(options.destination):
#if not os.path.exists(sys.argv[1]):
        #print "creating folder ", sys.argv
        os.makedirs(options.destination)

#for root, dirs, files in os.walk('.'):  # replace the . with your starting directory
for root, dirs, files in os.walk(options.target):
        for filename in files:
                path_file = os.path.abspath(os.path.join(root,filename))
                #destination_folder=options.destionation.rstrip("/")
                #path_file=path_file.replace(target_dirname, "")
                for file_ext in ext_list:

                        if path_file.endswith("." + file_ext):
                                target_path_to_copy=path_file.replace(target_dirname, "")
                                dest_path_to_copy=options.destination.rstrip("/") + "/" + target_path_to_copy.lstrip("/")
                                dest_path = os.path.dirname(dest_path_to_copy)
                                if not os.path.exists(dest_path):
                                        print("creating folder ", dest_path)
                                        os.makedirs(dest_path)

                                print("cp -u " + path_file + " " + dest_path_to_copy)
                                shutil.copy2(path_file, dest_path_to_copy)

exit(0)
