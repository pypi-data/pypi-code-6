#CoorTransform_GirdGeographic.py

"""
/***************************************************************************
Coordinate Transform between Gird and Geographic
 
								 A Python module
Provide functions for coordinate transform from grid to geographic, or vice versa
							 -------------------
		begin				: 2014-07-18
		copyright			: (C) 2014 by Walter Tsui
		email				: waltertech426@gmail.com
 ***************************************************************************/

/***************************************************************************
 *																		 *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or	 *
 *   (at your option) any later version.								   *
 *																		 *
 ***************************************************************************/
"""

#Coordinate Transformation according to http://www.geodetic.gov.hk/data/pdf/explanatorynotes_c.pdf

from math import * 


class CoorTransformer_GridAndGeographic:
	#HK80 Datum is set as default
	def __init__(self, E0 = 836694.05, N0 = 819069.8, Lng0 = 114.178556, Lat0 = 22.312133, m_0 = 1, M0 = 2468395.723, a = 6378388, e2 = 6.722670022 * pow(10,-3)):
		#Initilalize Projection Parameter
		self.E0 = E0
		self.N0 = N0
		self.Lng0 = Lng0 * pi / 180
		self.Lat0 = Lat0 * pi / 180
		self.m_0 = m_0
		self.M0 = M0
		self.a = a
		self.e2 = e2
		e4 = pow(e2, 2)

		
		#Meridian distance Coefficients
		self.A0 = 1 - (e2 / 4) - (3 * e4) / 64
		self.A2 = (3.0 / 8.0) * (e2 + (e4 / 4.0))
		self.A4 = (15.0 / 256.0) * e4
		
		
	def MeridianDist(self, Lat):
		return self.a * (self.A0 * Lat - self.A2 * sin(2 * Lat) + self.A4 * sin(4 * Lat))
		
		
	#Coordinate Transform from grid to geographic in degree
	def CoorTransform_GridToGeographic(self, Easting, Northing, accuracy = 9):
		E0 = self.E0
		N0 = self.N0
		Lng0 = self.Lng0
		Lat0 = self.Lat0
		m_0 = self.m_0
		M0 = self.M0
		a = self.a
		e2 = self.e2
		
		#Convert from grid to geographic
		#Calculate Lat_p by iteration of Meridian distance,
		E_Delta = Easting - E0
		N_delta = Northing - N0
		Mp = (N_delta + M0) / m_0
		
		Lat_min = -90 * pi / 180
		Lat_max = 90 * pi / 180

		accuracy = pow(10, -accuracy)
		M = 0
		
		while abs(M - Mp) > accuracy:
			Lat_p = (Lat_max + Lat_min) / 2
			M = self.MeridianDist(Lat_p)

			if M >= Mp:
				Lat_max = Lat_p
			else:
				Lat_min = Lat_p

		
		t_p = tan(Lat_p)
		v_p = a / pow((1.0 - e2 * pow(sin(Lat_p), 2)), (1 / 2))
		p_p = (a * (1.0 - e2)) / pow((1 - e2 * pow(sin(Lat_p), 2)), (3 / 2))
		W_p = v_p / p_p
		
		Lng = Lng0 + (1 / cos(Lat_p)) * ((E_Delta / (m_0 * v_p)) - (1 / 6) * pow((E_Delta / (m_0 * v_p)), 3) * (W_p + 2 * pow(t_p, 2)))
		Lat = Lat_p - (t_p / ((m_0 * p_p))) * (pow(E_Delta, 2) / ((2 * m_0 * v_p)))


		return [Lng / pi * 180, Lat / pi * 180]
		
		
	#Coordinate Transform from geographic in degree to grid
	def CoorTransform_GeographicToGrid(self, Lng, Lat):
		E0 = self.E0
		N0 = self.N0
		Lng0 = self.Lng0
		Lat0 = self.Lat0
		m_0 = self.m_0
		M0 = self.M0
		a = self.a
		e2 = self.e2
		
		#Convert Lat and Lng from degree to radian
		Lng = Lng * pi / 180
		Lat = Lat * pi / 180
		
		
		#Convert from geographic to grid
		Lng_Delta = Lng - Lng0
		M = self.MeridianDist(Lat)

		t_s = tan(Lat)
		v_s = a / pow((1.0 - e2 * pow(sin(Lat), 2)), (1 / 2))
		p_s = (a * (1.0 - e2)) / pow((1 - e2 * pow(sin(Lat), 2)), (3 / 2))
		W_s = v_s / p_s
		
		Easting = E0 + m_0 * v_s * (Lng_Delta * cos(Lat) + (1 / 6) * pow(Lng_Delta, 3) * pow(cos(Lat), 3) * pow(W_s - t_s, 2))
		Northing = N0 + m_0 * ((M - M0) + v_s * (pow(Lng_Delta, 2) / 4) * sin(2 * Lat))


		return [Easting, Northing]

		
	#Coordinate Transform from HK1980 grid to WGS84 geographic in degree
	def CoorTransform_Hk1980ToWgs84(self, Easting, Northing, Delimiter = ""):
		LngLat_HK1980 = self.CoorTransform_GridToGeographic(Easting, Northing)

		Lng_WGS84 = LngLat_HK1980[0] + (8.8 / 3600)
		Lat_WGS84 = LngLat_HK1980[1] - (5.5 / 3600)
		
		
		if Delimiter == "":
			return [Lng_WGS84, Lat_WGS84]
		else:
			return str(Lng_WGS84) + Delimiter + str(Lat_WGS84)

			
	#Coordinate Transform from WGS84 geographic in degree to HK1980 grid
	def CoorTransform_Wgs84ToHK1980(self, Lng, Lat, Delimiter = ""):
		Lng_HK1980 = Lng - (8.8 / 3600)
		Lat_HK1980 = Lat + (5.5 / 3600)
		
		EastNorth_HK1980 = self.CoorTransform_GeographicToGrid(Lng_HK1980, Lat_HK1980)
		
		
		if Delimiter == "":
			return EastNorth_HK1980
		else:
			return  str(EastNorth_HK1980(0)) & Delimiter & str(EastNorth_HK1980(1))
		
		