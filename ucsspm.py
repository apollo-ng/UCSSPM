#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
################################################################################
#
#  @file    ucsspm.py
#  @authors chrono
#  @version V1.0.2 (Argument Tamer)
#  @date    2014-11-10
#  @brief   Unified Clear-Sky Solar Prediction Model (UCSSPM)
#  @status  Beta - Request for Comment, Re-Verification & Enhancement
#
################################################################################
#  Copyright (c) 2014 Apollo-NG - https://apollo.open-resource.org/
################################################################################
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

import sys, argparse, math, time, calendar

################################################################################
##  Setup  #####################################################################
################################################################################

def setup(arg):

    # Set Solar Constant - See docs/solar-constant.pdf for more info. ##########
    # Default value of 1361.0 should IMHO serve as a good average point
    # between the min/max values over the 11-year sun cycle.

    arg.add_argument( "-sc"                                                    ,\
    type            = float                                                    ,\
    help            = "Solar Constant (@1AU) in kW/m² [Earth Default: 1361.0]" ,\
    default         = 1361.0                                                    )

    # Space/Time Pinpointing ###################################################

    arg.add_argument( "-lat"                                                   ,\
    type            = float                                                    ,\
    help            = "Latitude in decimal degrees [Default: 48.0]"            ,\
    default         = 48.0                                                      )

    arg.add_argument( "-lon"                                                   ,\
    type            = float                                                    ,\
    help            = "Longitude in decimal degrees [Default: 11.0]"           ,\
    default         = 11.0                                                      )

    # Optional, only needed if barometric pressure not available to compute it #

    arg.add_argument( "-alt"                                                   ,\
    type            = float                                                    ,\
    help            = "Altitude in meters above NN [Default: 0]"               ,\
    default         = 0                                                         )

    arg.add_argument( "-date"                                                  ,\
    type            = str                                                      ,\
    help            = "ISO Date YYYY-MM-DD [Default: "                          \
                    + time.strftime("%Y-%m-%d") + "]"                          ,\
    default         = time.strftime("%Y-%m-%d")                                 )

    arg.add_argument( "-time"                                                  ,\
    type            = str                                                      ,\
    help            = "ISO Time HH:MM:SS [Default: "                            \
                    + time.strftime("%H:%I:%S") + "]"                          ,\
    default         = time.strftime("%H:%I:%S")                                 )

    # Environmental Conditions #################################################

    arg.add_argument( "-at_t"                                                  ,\
    type            = float                                                    ,\
    help            = "Atmospheric Temperature in °C [Default: 25.0]"          ,\
    default         = 25.0                                                      )

    arg.add_argument( "-at_h"                                                  ,\
    type            = float                                                    ,\
    help            = "Atmospheric Relative Humidity in Percent [Default: 50]" ,\
    default         = 50.0                                                      )

    # Can be optional by submitting altitude - but will be less precise then ###

    arg.add_argument( "-at_p"                                                  ,\
    type            = float                                                    ,\
    help            = "Atmospheric Air Pressure in hPa [Default: Computed]"     )

    arg.add_argument( "-at_tc"                                                 ,\
    type            = float                                                    ,\
    help            = "Atmospheric Turbidity Coefficient [Default: 0.95]"      ,\
    default         = 0.95                                                      )

    # Photovoltaic Parameters ##################################################

    arg.add_argument( "-pv_a"                                                  ,\
    type            = float                                                    ,\
    help            = "Effective PV Panel Surface in m² [Default: 1.67]"       ,\
    default         = 1.67                                                      )

    arg.add_argument( "-pv_e"                                                  ,\
    type            = float                                                    ,\
    help            = "PV Panel Efficiency in Percent [Default: 16]"           ,\
    default         = 16                                                        )

    arg.add_argument( "-pv_t"                                                  ,\
    type            = float                                                    ,\
    help            = "PV Panel Temperature in °C [Default: 25.0]"             ,\
    default         = 25.0                                                      )

    arg.add_argument( "-pv_tc"                                                 ,\
    type            = float                                                    ,\
    help            = "PV Panel negative Temp. Coefficient [Default: 0.35]"    ,\
    default         = 0.35                                                      )

    arg.add_argument( "-pv_ac"                                                 ,\
    type            = float                                                    ,\
    help            = "PV Panel age related Coefficient [Default: 0.98]"       ,\
    default         = 0.98                                                      )

################################################################################
##  MAIN  ######################################################################
################################################################################

def main():

    arg             = argparse.ArgumentParser()
    setup           (arg)
    options         = arg.parse_args()

    odate           = options.date.split("-")
    year            = int(odate[0])
    month           = int(odate[1])
    day             = int(odate[2])

    otime           = options.time.split(":")
    hour            = int(otime[0])
    min             = int(otime[1])
    sec             = int(otime[2])
    ToD             = hour

    dst_off         = 0
    tz_off_deg      = 0 + options.lon

    # get Julian Day (Day of Year)

    if              calendar.isleap(year):

        # Leap year (366 days)
        lMonth      = [0,31,60,91,121,152,182,213,244,274,305,335,366]

    else:

        # Normal year (365 days)
        lMonth      = [0,31,59,90,120,151,181,212,243,273,304,334,365]

    DoY             = lMonth[month-1] + day

    print "--------------------------------------------------------------"

    print "%d.%d.%d | %d | %f | " % (day, month, year, DoY, ToD )

    print "--------------------------------------------------------------"

    print "Solar Constant                               : %s" % options.sc
    print "Atmospheric turbidity coefficient            : %s" % options.at_tc

    print "--------------------------------------------------------------"


    # Compute inverse relative distance factor (Distance between Earth and Sun)

    sun_rel_dist_f  = 1.0/(1.0-9.464e-4*math.sin(DoY)-                      \
                    + 0.01671*math.cos(DoY)-                                \
                    + 1.489e-4*math.cos(2.0*DoY)-2.917e-5*math.sin(3.0*DoY)-\
                    + 3.438e-4*math.cos(4.0*DoY))**2

    print "Inverse relative distance factor             : %s" % sun_rel_dist_f

    # Compute solar declination ################################################

    sun_decl        = (math.asin(0.39785*(math.sin(((278.97+(0.9856*DoY))   \
                    + (1.9165*(math.sin((356.6+(0.9856*DoY))                \
                    * (math.pi/180)))))*(math.pi/180))))*180)               \
                    / math.pi


    print "Sun declination                              : %s°" % sun_decl


    # Solve equation of time ###################################################
    # (More info on http://www.srrb.noaa.gov/highlights/sunrise/azel.html)

    eqt             = (((5.0323-(430.847*math.cos((((2*math.pi)*DoY)/366)+4.8718)))\
                    + (12.5024*(math.cos(2*((((2*math.pi)*DoY)/366)+4.8718))))\
                    + (18.25*(math.cos(3*((((2*math.pi)*DoY)/366)+4.8718))))\
                    - (100.976*(math.sin((((2*math.pi)*DoY)/366)+4.8718))))\
                    + (595.275*(math.sin(2*((((2*math.pi)*DoY)/366)+4.8718))))\
                    + (3.6858*(math.sin(3*((((2*math.pi)*DoY)/366)+4.871))))\
                    - (12.47*(math.sin(4*((((2*math.pi)*DoY)/366)+4.8718)))))\
                    / 60

    print "Equation of time                             : %s min" % eqt


    # time of solar noon ###################################################

    sol_noon        = ((12+dst_off)-(eqt/60))-((tz_off_deg-options.lon)/15)

    print "Solar Noon                                   : %s " % sol_noon


    # solar zenith angle in DEG ############################################

    sol_zen         = math.acos(((math.sin(options.lat*(math.pi/180)))        \
                    * (math.sin(sun_decl*(math.pi/180))))                       \
                    + (((math.cos(options.lat*((math.pi/180))))               \
                    * (math.cos(sun_decl*(math.pi/180))))                       \
                    * (math.cos((ToD-sol_noon)*(math.pi/12)))))                 \
                    * (180/math.pi)

    # in extreme latitude, values over 90 may occurs.
    if sol_zen > 90:
        sol_zen     = 90

    print "Solar Zenith Angle                           : %s° " % sol_zen


    # Barometric pressure of the measurement site
    # (this should be replaced by the real measured value) in kPa

    atm_press       = 101.325                                                   \
                    * math.pow(((288-(0.0065*(options.alt-0)))/288)           \
                    , (9.80665/(0.0065*287)))

    atm_press       = 100.5

    print "Estimated Barometric Pressure at site        : %s kPa" % atm_press


    # Estimated air vapor pressure in kPa ###################################

    atm_vapor_press = (0.61121*math.exp((17.502*options.at_t)                   \
                    / (240.97+options.at_t)))                                   \
                    * (options.at_h/100)

    print "Estimated Vapor Pressure at site             : %s kPa" % atm_vapor_press


    # Extraterrestrial radiation in W/m2 ###################################

    extra_terr_rad  = (options.sc*sun_rel_dist_f)                            \
                    * (math.cos(sol_zen*(math.pi/180)))

    print "Estimated Extraterrestrial radiation         : %s W/m²" % extra_terr_rad


    # Precipitable water in the atmosphere in mm ###########################

    atm_prec_h2o    = ((0.14*atm_vapor_press)*atm_press)+2.1

    print "Estimated precipitable water in Atmosphere   : %s mm" % atm_prec_h2o


    # Clearness index for direct beam radiation [unitless] #################

    clr_idx_beam_rad= 0.98*(math.exp(((-0.00146*atm_press)                  \
                    / (options.at_tc*(math.sin((90-sol_zen)*(math.pi/180)))))      \
                    - (0.075*(math.pow((atm_prec_h2o                        \
                    / (math.sin((90-sol_zen)*(math.pi/180)))),0.4)))))

    print "Clearness index for direct beam radiation    : %s" % clr_idx_beam_rad


    # Transmissivity index for diffuse radiation [unitless] ####################

    if                              (clr_idx_beam_rad > 0.15):
        trns_idx_diff_rad=          0.35-(0.36*clr_idx_beam_rad)
    else:
        trns_idx_diff_rad=          0.18+(0.82*clr_idx_beam_rad)

    print "Transmissivity index for diffuse radiation   : %s" % trns_idx_diff_rad


    # Model Estimated Shortwave Radiation (W/m2) ###############################

    est_sol_rad     =               (clr_idx_beam_rad + trns_idx_diff_rad)      \
                    *               extra_terr_rad

    print "--------------------------------------------------------------"
    print "Model Estimated Shortwave Radiation (RSO)    : \033[1;33m%3.1f W/m²\033[0m" % est_sol_rad

    # Optimal PV Module Angle to Sun

    print "Optimum elevation of PV-Panel                : \033[1;37m%02.1f°\033[0m" % sol_zen


    # Estimate Theoretical Max. Power Output (Panel at nominal Efficiency) #####

    est_p_out       =               (est_sol_rad * options.pv_a)                \
                    /               100 * options.pv_e

    print "Model Estimated Max. PV-Power Output         : \033[1;32m%3.1f W\033[0m \033[1;37m@ %d%% Mod Eff\033[0m" % (est_p_out, options.pv_e)

    # Estimate conversion loss due to module temperature ###################

    pv_p_loss       =               (options.pv_t-25 ) * options.pv_tc
    pv_p_loss_p     =               (est_p_out/100) * pv_p_loss

    print "Model estimated PV-Module temp conv. loss    : -\033[1;31m%2.1f W / %2.1f%%\033[0m" % (pv_p_loss_p, pv_p_loss)

    # Estimate conversion loss due to module age

    est_pv_age_loss =               est_p_out - (est_p_out * options.pv_ac)

    print "Model estimated PV-Module aging loss         : -\033[1;31m%03.1f W\033[0m" % est_pv_age_loss

    # Estime final System Power output

    est_real_p_out  =               est_p_out - est_pv_age_loss-pv_p_loss_p

    print "--------------------------------------------------------------"
    print "Model Estimated Real PV-Power Output         : \033[1;32m%3.1f W\033[0m" % est_real_p_out

    return 0

################################################################################

if __name__ == '__main__':
    rc              = main          ()
    sys.exit                        (rc)
