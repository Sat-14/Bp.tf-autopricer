#!/bin/bash
sudo apt install pymongo
uvicorn fast:pricer --reload
