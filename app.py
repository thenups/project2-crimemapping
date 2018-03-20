#################################################
# Dependencies
#################################################
import numpy as np

from flask import Flask, render_template, jsonify, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect, Column, Integer, String

import os
from flask_sqlalchemy import SQLAlchemy


## Hi my name is nupur
