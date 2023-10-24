# Project workflow

## Main Thread

Handles 3 sub threads

 * Modbus Server
 * Log Watcher
 * Records Ingestor

 ## Modbus Server

 The purpose of having a Modbus server running in the raspberry, is to stablish communication with the I/O of the HMI, mainly with the Digital Outputs, to provide feedback of the status and responses of the other threads, so the raspberry activates or deactivates signals that will be visible as LEDs in the HMI device.

 ## Log Watcher

 Stablish ftp connection to the ftp server in the HMI and the constantly scans for new logs and downloads them into a specific path for each kind of log

 ## Record Ingestor

This Constantly scans the download path, so that each time a new log file is downloaded, sends its record information to the corresponding database.