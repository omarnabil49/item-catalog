# Items Catalog

## Project Setup

1. Install VirtualBox tool.

   https://www.virtualbox.org/wiki/Downloads

2. Install Vagrant tool.

   https://www.vagrantup.com/downloads.html

3. Download the virtual machine configuration 

   https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip
	
   or use Github to fork and clone the repository. 

   https://github.com/udacity/fullstack-nanodegree-vm

4. Using your terminal and `cd` command change directory to vagrant folder in the downloaded directory.

5. Download itemCatalog zip file and extract and move it to the vagrant directory.

6. Start virtual machine by running `vagrant up` command.

7. Login into the virtual machine using `vagrant ssh`.

8. `cd` to the extracted directory

9. Run `database_setup.py` to setup the database.

10. Run `lotsofseries.py` to insert data to the database.

11. Run `application.py` to start the application.

12. Use `http://localhost:8000` to start accessing the application.