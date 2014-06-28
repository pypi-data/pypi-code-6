from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///data.sqlite')
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata.bind = engine
Base.query = session.query_property()

taxinfo_ud = Table('taxinfo_ud', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('ud_id', Integer, ForeignKey('ud.id')))

taxinfo_yq = Table('taxinfo_yq', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yq_id', Integer, ForeignKey('yq.id')))

iz__taxinfo = Table('iz__taxinfo', Base.metadata
  ,Column('iz__id', Integer, ForeignKey('iz_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

taxinfo_vl = Table('taxinfo_vl', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('vl_id', Integer, ForeignKey('vl.id')))

_t_fareinfo = Table('_t_fareinfo', Base.metadata
  ,Column('_t_id', Integer, ForeignKey('_t.id'))
  ,Column('fareinfo_id', Integer, ForeignKey('fareinfo.id')))

geocodes_itemdetails = Table('geocodes_itemdetails', Base.metadata
  ,Column('geocodes_id', Integer, ForeignKey('geocodes.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

taxinfo_zo_ = Table('taxinfo_zo_', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('zo__id', Integer, ForeignKey('zo_.id')))

bg_taxinfo = Table('bg_taxinfo', Base.metadata
  ,Column('bg_id', Integer, ForeignKey('bg.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

ffilter_start_end = Table('ffilter_start_end', Base.metadata
  ,Column('ffilter_id', Integer, ForeignKey('ffilter.id'))
  ,Column('start_end_id', Integer, ForeignKey('start_end.id')))

dep_itemdetails = Table('dep_itemdetails', Base.metadata
  ,Column('dep_id', Integer, ForeignKey('dep.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

de__taxinfo = Table('de__taxinfo', Base.metadata
  ,Column('de__id', Integer, ForeignKey('de_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

__itemdetails = Table('__itemdetails', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

data_required_parameters = Table('data_required_parameters', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('required_parameters_id', Integer, ForeignKey('required_parameters.id')))

taxinfo_yrf = Table('taxinfo_yrf', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yrf_id', Integer, ForeignKey('yrf.id')))

hb_taxinfo = Table('hb_taxinfo', Base.metadata
  ,Column('hb_id', Integer, ForeignKey('hb.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

geocodes_info = Table('geocodes_info', Base.metadata
  ,Column('geocodes_id', Integer, ForeignKey('geocodes.id'))
  ,Column('info_id', Integer, ForeignKey('info.id')))

taxinfo_yk = Table('taxinfo_yk', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yk_id', Integer, ForeignKey('yk.id')))

taxinfo_yri = Table('taxinfo_yri', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yri_id', Integer, ForeignKey('yri.id')))

baggage_allowance_ods_ist = Table('baggage_allowance_ods_ist', Base.metadata
  ,Column('baggage_allowance_id', Integer, ForeignKey('baggage_allowance.id'))
  ,Column('ods_ist_id', Integer, ForeignKey('ods_ist.id')))

dateofbirthisnotrequiredforadults_per_booking = Table('dateofbirthisnotrequiredforadults_per_booking', Base.metadata
  ,Column('dateofbirthisnotrequiredforadults_id', Integer, ForeignKey('dateofbirthisnotrequiredforadults.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

dateofbirthadult_per_pax = Table('dateofbirthadult_per_pax', Base.metadata
  ,Column('dateofbirthadult_id', Integer, ForeignKey('dateofbirthadult.id'))
  ,Column('per_pax_id', Integer, ForeignKey('per_pax.id')))

ro_taxinfo = Table('ro_taxinfo', Base.metadata
  ,Column('ro_id', Integer, ForeignKey('ro.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

adult_farebasis = Table('adult_farebasis', Base.metadata
  ,Column('adult_id', Integer, ForeignKey('adult.id'))
  ,Column('farebasis_id', Integer, ForeignKey('farebasis.id')))

data_error = Table('data_error', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('error_id', Integer, ForeignKey('error.id')))

taxinfo_yqi = Table('taxinfo_yqi', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yqi_id', Integer, ForeignKey('yqi.id')))

dep_landing = Table('dep_landing', Base.metadata
  ,Column('dep_id', Integer, ForeignKey('dep.id'))
  ,Column('landing_id', Integer, ForeignKey('landing.id')))

per_booking_postcode = Table('per_booking_postcode', Base.metadata
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id'))
  ,Column('postcode_id', Integer, ForeignKey('postcode.id')))

taxinfo_us_ = Table('taxinfo_us_', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('us__id', Integer, ForeignKey('us_.id')))

data_price = Table('data_price', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

numberofbags_per_pax = Table('numberofbags_per_pax', Base.metadata
  ,Column('numberofbags_id', Integer, ForeignKey('numberofbags.id'))
  ,Column('per_pax_id', Integer, ForeignKey('per_pax.id')))

cardsecuritynumber_per_booking = Table('cardsecuritynumber_per_booking', Base.metadata
  ,Column('cardsecuritynumber_id', Integer, ForeignKey('cardsecuritynumber.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

ratings_service = Table('ratings_service', Base.metadata
  ,Column('ratings_id', Integer, ForeignKey('ratings.id'))
  ,Column('service_id', Integer, ForeignKey('service.id')))

___price = Table('___price', Base.metadata
  ,Column('___id', Integer, ForeignKey('__.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

ret_takeoff = Table('ret_takeoff', Base.metadata
  ,Column('ret_id', Integer, ForeignKey('ret.id'))
  ,Column('takeoff_id', Integer, ForeignKey('takeoff.id')))

dep_takeoff = Table('dep_takeoff', Base.metadata
  ,Column('dep_id', Integer, ForeignKey('dep.id'))
  ,Column('takeoff_id', Integer, ForeignKey('takeoff.id')))

data_data = Table('data_data', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('data_id', Integer, ForeignKey('data.id')))

jk_taxinfo = Table('jk_taxinfo', Base.metadata
  ,Column('jk_id', Integer, ForeignKey('jk.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

child_svcbreakdown = Table('child_svcbreakdown', Base.metadata
  ,Column('child_id', Integer, ForeignKey('child.id'))
  ,Column('svcbreakdown_id', Integer, ForeignKey('svcbreakdown.id')))

fr__taxinfo = Table('fr__taxinfo', Base.metadata
  ,Column('fr__id', Integer, ForeignKey('fr_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

___itemdetails = Table('___itemdetails', Base.metadata
  ,Column('___id', Integer, ForeignKey('__.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

data_sort = Table('data_sort', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('sort_id', Integer, ForeignKey('sort.id')))

per_booking_prepaycustomersourceidentifier = Table('per_booking_prepaycustomersourceidentifier', Base.metadata
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id'))
  ,Column('prepaycustomersourceidentifier_id', Integer, ForeignKey('prepaycustomersourceidentifier.id')))

baggage_allowance_price = Table('baggage_allowance_price', Base.metadata
  ,Column('baggage_allowance_id', Integer, ForeignKey('baggage_allowance.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

data_ffilter = Table('data_ffilter', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('ffilter_id', Integer, ForeignKey('ffilter.id')))

_____itemdetails = Table('_____itemdetails', Base.metadata
  ,Column('_____id', Integer, ForeignKey('____.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

taxinfo_xf = Table('taxinfo_xf', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('xf_id', Integer, ForeignKey('xf.id')))

taxinfo_vv = Table('taxinfo_vv', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('vv_id', Integer, ForeignKey('vv.id')))

taxinfo_yqf = Table('taxinfo_yqf', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yqf_id', Integer, ForeignKey('yqf.id')))

se_taxinfo = Table('se_taxinfo', Base.metadata
  ,Column('se_id', Integer, ForeignKey('se.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

originalprice_price = Table('originalprice_price', Base.metadata
  ,Column('originalprice_id', Integer, ForeignKey('originalprice.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

per_booking_phonecountrycode = Table('per_booking_phonecountrycode', Base.metadata
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id'))
  ,Column('phonecountrycode_id', Integer, ForeignKey('phonecountrycode.id')))

qh_taxinfo = Table('qh_taxinfo', Base.metadata
  ,Column('qh_id', Integer, ForeignKey('qh.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

details_farebasis = Table('details_farebasis', Base.metadata
  ,Column('details_id', Integer, ForeignKey('details.id'))
  ,Column('farebasis_id', Integer, ForeignKey('farebasis.id')))

baggage_allowance_hrg_iev = Table('baggage_allowance_hrg_iev', Base.metadata
  ,Column('baggage_allowance_id', Integer, ForeignKey('baggage_allowance.id'))
  ,Column('hrg_iev_id', Integer, ForeignKey('hrg_iev.id')))

adult_originalprice = Table('adult_originalprice', Base.metadata
  ,Column('adult_id', Integer, ForeignKey('adult.id'))
  ,Column('originalprice_id', Integer, ForeignKey('originalprice.id')))

ca__taxinfo = Table('ca__taxinfo', Base.metadata
  ,Column('ca__id', Integer, ForeignKey('ca_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

_____items = Table('_____items', Base.metadata
  ,Column('_____id', Integer, ForeignKey('____.id'))
  ,Column('items_id', Integer, ForeignKey('items.id')))

____items = Table('____items', Base.metadata
  ,Column('____id', Integer, ForeignKey('___.id'))
  ,Column('items_id', Integer, ForeignKey('items.id')))

price_ratings = Table('price_ratings', Base.metadata
  ,Column('price_id', Integer, ForeignKey('price.id'))
  ,Column('ratings_id', Integer, ForeignKey('ratings.id')))

info_roomtypes = Table('info_roomtypes', Base.metadata
  ,Column('info_id', Integer, ForeignKey('info.id'))
  ,Column('roomtypes_id', Integer, ForeignKey('roomtypes.id')))

adult_svcbreakdown = Table('adult_svcbreakdown', Base.metadata
  ,Column('adult_id', Integer, ForeignKey('adult.id'))
  ,Column('svcbreakdown_id', Integer, ForeignKey('svcbreakdown.id')))

qx__taxinfo = Table('qx__taxinfo', Base.metadata
  ,Column('qx__id', Integer, ForeignKey('qx_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

itemdetails_ratings = Table('itemdetails_ratings', Base.metadata
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id'))
  ,Column('ratings_id', Integer, ForeignKey('ratings.id')))

____price = Table('____price', Base.metadata
  ,Column('____id', Integer, ForeignKey('___.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

at_taxinfo = Table('at_taxinfo', Base.metadata
  ,Column('at_id', Integer, ForeignKey('at.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

info_itemdetails = Table('info_itemdetails', Base.metadata
  ,Column('info_id', Integer, ForeignKey('info.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

airport_ffilter = Table('airport_ffilter', Base.metadata
  ,Column('airport_id', Integer, ForeignKey('airport.id'))
  ,Column('ffilter_id', Integer, ForeignKey('ffilter.id')))

ra__taxinfo = Table('ra__taxinfo', Base.metadata
  ,Column('ra__id', Integer, ForeignKey('ra_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

____itemdetails = Table('____itemdetails', Base.metadata
  ,Column('____id', Integer, ForeignKey('___.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

taxinfo_us = Table('taxinfo_us', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('us_id', Integer, ForeignKey('us.id')))

__t_fareinfo = Table('__t_fareinfo', Base.metadata
  ,Column('__t_id', Integer, ForeignKey('__t.id'))
  ,Column('fareinfo_id', Integer, ForeignKey('fareinfo.id')))

taxinfo_zn = Table('taxinfo_zn', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('zn_id', Integer, ForeignKey('zn.id')))

__adult = Table('__adult', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('adult_id', Integer, ForeignKey('adult.id')))

__ret = Table('__ret', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('ret_id', Integer, ForeignKey('ret.id')))

ret_start_end = Table('ret_start_end', Base.metadata
  ,Column('ret_id', Integer, ForeignKey('ret.id'))
  ,Column('start_end_id', Integer, ForeignKey('start_end.id')))

taxinfo_zy = Table('taxinfo_zy', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('zy_id', Integer, ForeignKey('zy.id')))

__dep = Table('__dep', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('dep_id', Integer, ForeignKey('dep.id')))

itemdetails_location = Table('itemdetails_location', Base.metadata
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id'))
  ,Column('location_id', Integer, ForeignKey('location.id')))

data_itemdetails = Table('data_itemdetails', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

rn_taxinfo = Table('rn_taxinfo', Base.metadata
  ,Column('rn_id', Integer, ForeignKey('rn.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

dep_start_end = Table('dep_start_end', Base.metadata
  ,Column('dep_id', Integer, ForeignKey('dep.id'))
  ,Column('start_end_id', Integer, ForeignKey('start_end.id')))

child_originalprice = Table('child_originalprice', Base.metadata
  ,Column('child_id', Integer, ForeignKey('child.id'))
  ,Column('originalprice_id', Integer, ForeignKey('originalprice.id')))

farebasis_price = Table('farebasis_price', Base.metadata
  ,Column('farebasis_id', Integer, ForeignKey('farebasis.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

details_price = Table('details_price', Base.metadata
  ,Column('details_id', Integer, ForeignKey('details.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

ad_taxinfo = Table('ad_taxinfo', Base.metadata
  ,Column('ad_id', Integer, ForeignKey('ad.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

item_itemdetails = Table('item_itemdetails', Base.metadata
  ,Column('item_id', Integer, ForeignKey('item.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

__cardtypes = Table('__cardtypes', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('cardtypes_id', Integer, ForeignKey('cardtypes.id')))

__items = Table('__items', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('items_id', Integer, ForeignKey('items.id')))

taxinfo_ua = Table('taxinfo_ua', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('ua_id', Integer, ForeignKey('ua.id')))

data_items = Table('data_items', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('items_id', Integer, ForeignKey('items.id')))

taxinfo_yc = Table('taxinfo_yc', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yc_id', Integer, ForeignKey('yc.id')))

fe_taxinfo = Table('fe_taxinfo', Base.metadata
  ,Column('fe_id', Integer, ForeignKey('fe.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

per_booking_usetfprepay = Table('per_booking_usetfprepay', Base.metadata
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id'))
  ,Column('usetfprepay_id', Integer, ForeignKey('usetfprepay.id')))

baggage_allowance_ist_ods = Table('baggage_allowance_ist_ods', Base.metadata
  ,Column('baggage_allowance_id', Integer, ForeignKey('baggage_allowance.id'))
  ,Column('ist_ods_id', Integer, ForeignKey('ist_ods.id')))

child_details = Table('child_details', Base.metadata
  ,Column('child_id', Integer, ForeignKey('child.id'))
  ,Column('details_id', Integer, ForeignKey('details.id')))

___items = Table('___items', Base.metadata
  ,Column('___id', Integer, ForeignKey('__.id'))
  ,Column('items_id', Integer, ForeignKey('items.id')))

data_filter = Table('data_filter', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('filter_id', Integer, ForeignKey('filter.id')))

sq__taxinfo = Table('sq__taxinfo', Base.metadata
  ,Column('sq__id', Integer, ForeignKey('sq_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

per_booking_required_parameters = Table('per_booking_required_parameters', Base.metadata
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id'))
  ,Column('required_parameters_id', Integer, ForeignKey('required_parameters.id')))

taxinfo_xy = Table('taxinfo_xy', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('xy_id', Integer, ForeignKey('xy.id')))

hu_taxinfo = Table('hu_taxinfo', Base.metadata
  ,Column('hu_id', Integer, ForeignKey('hu.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

oy_taxinfo = Table('oy_taxinfo', Base.metadata
  ,Column('oy_id', Integer, ForeignKey('oy.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

data_rank_details = Table('data_rank_details', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('rank_details_id', Integer, ForeignKey('rank_details.id')))

city_itemdetails = Table('city_itemdetails', Base.metadata
  ,Column('city_id', Integer, ForeignKey('city.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

adult_details = Table('adult_details', Base.metadata
  ,Column('adult_id', Integer, ForeignKey('adult.id'))
  ,Column('details_id', Integer, ForeignKey('details.id')))

it__taxinfo = Table('it__taxinfo', Base.metadata
  ,Column('it__id', Integer, ForeignKey('it_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

filter_price = Table('filter_price', Base.metadata
  ,Column('filter_id', Integer, ForeignKey('filter.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

ffilter_waiting = Table('ffilter_waiting', Base.metadata
  ,Column('ffilter_id', Integer, ForeignKey('ffilter.id'))
  ,Column('waiting_id', Integer, ForeignKey('waiting.id')))

taxinfo_vt = Table('taxinfo_vt', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('vt_id', Integer, ForeignKey('vt.id')))

rc__taxinfo = Table('rc__taxinfo', Base.metadata
  ,Column('rc__id', Integer, ForeignKey('rc_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

cj_taxinfo = Table('cj_taxinfo', Base.metadata
  ,Column('cj_id', Integer, ForeignKey('cj.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

filter_gmap = Table('filter_gmap', Base.metadata
  ,Column('filter_id', Integer, ForeignKey('filter.id'))
  ,Column('gmap_id', Integer, ForeignKey('gmap.id')))

ffilter_fprice = Table('ffilter_fprice', Base.metadata
  ,Column('ffilter_id', Integer, ForeignKey('ffilter.id'))
  ,Column('fprice_id', Integer, ForeignKey('fprice.id')))

taxinfo_ux = Table('taxinfo_ux', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('ux_id', Integer, ForeignKey('ux.id')))

data_different_checkin = Table('data_different_checkin', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('different_checkin_id', Integer, ForeignKey('different_checkin.id')))

per_booking_phoneareacode = Table('per_booking_phoneareacode', Base.metadata
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id'))
  ,Column('phoneareacode_id', Integer, ForeignKey('phoneareacode.id')))

_____price = Table('_____price', Base.metadata
  ,Column('_____id', Integer, ForeignKey('____.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

ap_taxinfo = Table('ap_taxinfo', Base.metadata
  ,Column('ap_id', Integer, ForeignKey('ap.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

ay_taxinfo = Table('ay_taxinfo', Base.metadata
  ,Column('ay_id', Integer, ForeignKey('ay.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

per_pax_required_parameters = Table('per_pax_required_parameters', Base.metadata
  ,Column('per_pax_id', Integer, ForeignKey('per_pax.id'))
  ,Column('required_parameters_id', Integer, ForeignKey('required_parameters.id')))

distance_filter = Table('distance_filter', Base.metadata
  ,Column('distance_id', Integer, ForeignKey('distance.id'))
  ,Column('filter_id', Integer, ForeignKey('filter.id')))

taxinfo_tr = Table('taxinfo_tr', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('tr_id', Integer, ForeignKey('tr.id')))

adult_fareinfo = Table('adult_fareinfo', Base.metadata
  ,Column('adult_id', Integer, ForeignKey('adult.id'))
  ,Column('fareinfo_id', Integer, ForeignKey('fareinfo.id')))

distance_itemdetails = Table('distance_itemdetails', Base.metadata
  ,Column('distance_id', Integer, ForeignKey('distance.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

dc_taxinfo = Table('dc_taxinfo', Base.metadata
  ,Column('dc_id', Integer, ForeignKey('dc.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

___ = Table('___', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('__id', Integer, ForeignKey('_.id')))

baggageweight_per_pax = Table('baggageweight_per_pax', Base.metadata
  ,Column('baggageweight_id', Integer, ForeignKey('baggageweight.id'))
  ,Column('per_pax_id', Integer, ForeignKey('per_pax.id')))

extrainfo_itemdetails = Table('extrainfo_itemdetails', Base.metadata
  ,Column('extrainfo_id', Integer, ForeignKey('extrainfo.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

itemdetails_ret = Table('itemdetails_ret', Base.metadata
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id'))
  ,Column('ret_id', Integer, ForeignKey('ret.id')))

itemdetails_lccterms = Table('itemdetails_lccterms', Base.metadata
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id'))
  ,Column('lccterms_id', Integer, ForeignKey('lccterms.id')))

rd__taxinfo = Table('rd__taxinfo', Base.metadata
  ,Column('rd__id', Integer, ForeignKey('rd_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

baggage_allowance_data = Table('baggage_allowance_data', Base.metadata
  ,Column('baggage_allowance_id', Integer, ForeignKey('baggage_allowance.id'))
  ,Column('data_id', Integer, ForeignKey('data.id')))

adult_taxinfo = Table('adult_taxinfo', Base.metadata
  ,Column('adult_id', Integer, ForeignKey('adult.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

fareinfo_price = Table('fareinfo_price', Base.metadata
  ,Column('fareinfo_id', Integer, ForeignKey('fareinfo.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

__t_baggageallowance = Table('__t_baggageallowance', Base.metadata
  ,Column('__t_id', Integer, ForeignKey('__t.id'))
  ,Column('baggageallowance_id', Integer, ForeignKey('baggageallowance.id')))

mj_taxinfo = Table('mj_taxinfo', Base.metadata
  ,Column('mj_id', Integer, ForeignKey('mj.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

breakdown_price = Table('breakdown_price', Base.metadata
  ,Column('breakdown_id', Integer, ForeignKey('breakdown.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

data_fsort = Table('data_fsort', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('fsort_id', Integer, ForeignKey('fsort.id')))

taxinfo_ub = Table('taxinfo_ub', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('ub_id', Integer, ForeignKey('ub.id')))

ratings_room = Table('ratings_room', Base.metadata
  ,Column('ratings_id', Integer, ForeignKey('ratings.id'))
  ,Column('room_id', Integer, ForeignKey('room.id')))

info_itemfacility = Table('info_itemfacility', Base.metadata
  ,Column('info_id', Integer, ForeignKey('info.id'))
  ,Column('itemfacility_id', Integer, ForeignKey('itemfacility.id')))

aa_taxinfo = Table('aa_taxinfo', Base.metadata
  ,Column('aa_id', Integer, ForeignKey('aa.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

lb__taxinfo = Table('lb__taxinfo', Base.metadata
  ,Column('lb__id', Integer, ForeignKey('lb_.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

childrenandinfantsbooking_per_booking = Table('childrenandinfantsbooking_per_booking', Base.metadata
  ,Column('childrenandinfantsbooking_id', Integer, ForeignKey('childrenandinfantsbooking.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

info_roomfacility = Table('info_roomfacility', Base.metadata
  ,Column('info_id', Integer, ForeignKey('info.id'))
  ,Column('roomfacility_id', Integer, ForeignKey('roomfacility.id')))

itemdetails_ticketrules = Table('itemdetails_ticketrules', Base.metadata
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id'))
  ,Column('ticketrules_id', Integer, ForeignKey('ticketrules.id')))

taxinfo_zf = Table('taxinfo_zf', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('zf_id', Integer, ForeignKey('zf.id')))

fullcardnamebreakdown_per_booking = Table('fullcardnamebreakdown_per_booking', Base.metadata
  ,Column('fullcardnamebreakdown_id', Integer, ForeignKey('fullcardnamebreakdown.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

__price = Table('__price', Base.metadata
  ,Column('__id', Integer, ForeignKey('_.id'))
  ,Column('price_id', Integer, ForeignKey('price.id')))

landing_ret = Table('landing_ret', Base.metadata
  ,Column('landing_id', Integer, ForeignKey('landing.id'))
  ,Column('ret_id', Integer, ForeignKey('ret.id')))

info_text = Table('info_text', Base.metadata
  ,Column('info_id', Integer, ForeignKey('info.id'))
  ,Column('text_id', Integer, ForeignKey('text.id')))

taxinfo_yr = Table('taxinfo_yr', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('yr_id', Integer, ForeignKey('yr.id')))

dateofbirth_per_pax = Table('dateofbirth_per_pax', Base.metadata
  ,Column('dateofbirth_id', Integer, ForeignKey('dateofbirth.id'))
  ,Column('per_pax_id', Integer, ForeignKey('per_pax.id')))

cz_taxinfo = Table('cz_taxinfo', Base.metadata
  ,Column('cz_id', Integer, ForeignKey('cz.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

billingaddress_per_booking = Table('billingaddress_per_booking', Base.metadata
  ,Column('billingaddress_id', Integer, ForeignKey('billingaddress.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

taxinfo_vb = Table('taxinfo_vb', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('vb_id', Integer, ForeignKey('vb.id')))

ae_taxinfo = Table('ae_taxinfo', Base.metadata
  ,Column('ae_id', Integer, ForeignKey('ae.id'))
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id')))

taxinfo_xa = Table('taxinfo_xa', Base.metadata
  ,Column('taxinfo_id', Integer, ForeignKey('taxinfo.id'))
  ,Column('xa_id', Integer, ForeignKey('xa.id')))

childrenandinfantssearch_per_booking = Table('childrenandinfantssearch_per_booking', Base.metadata
  ,Column('childrenandinfantssearch_id', Integer, ForeignKey('childrenandinfantssearch.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

mobilephone_per_booking = Table('mobilephone_per_booking', Base.metadata
  ,Column('mobilephone_id', Integer, ForeignKey('mobilephone.id'))
  ,Column('per_booking_id', Integer, ForeignKey('per_booking.id')))

cardtypes_itemdetails = Table('cardtypes_itemdetails', Base.metadata
  ,Column('cardtypes_id', Integer, ForeignKey('cardtypes.id'))
  ,Column('itemdetails_id', Integer, ForeignKey('itemdetails.id')))

baggage_allowance_iev_hrg = Table('baggage_allowance_iev_hrg', Base.metadata
  ,Column('baggage_allowance_id', Integer, ForeignKey('baggage_allowance.id'))
  ,Column('iev_hrg_id', Integer, ForeignKey('iev_hrg.id')))

data_extras = Table('data_extras', Base.metadata
  ,Column('data_id', Integer, ForeignKey('data.id'))
  ,Column('extras_id', Integer, ForeignKey('extras.id')))

ratings_staff = Table('ratings_staff', Base.metadata
  ,Column('ratings_id', Integer, ForeignKey('ratings.id'))
  ,Column('staff_id', Integer, ForeignKey('staff.id')))

class __(Base):
    __tablename__ = '__'
    id = Column(Integer, primary_key=True)
    roomid = Column(String)
    itemcode = Column(String)
    city = Column(String)
    hotelsearchcode = Column(String)
    gtaitemcode = Column(String)
    hotelcode = Column(Integer)
    tf_supplier = Column(String)
    id = Column(Integer)
    classid = Column(String)
    class = Column(String)
    prices = relationship('Price', secondary=___price)
    itemdetailss = relationship('Itemdetails', secondary=___itemdetails)
    itemss = relationship('Items', secondary=___items)

    def __init__(self, classid=None, city=None, hotelcode=None, gtaitemcode=None, id=None, itemcode=None, hotelsearchcode=None, roomid=None, class=None, tf_supplier=None):
        self.classid = classid
        self.city = city
        self.hotelcode = hotelcode
        self.gtaitemcode = gtaitemcode
        self.id = id
        self.itemcode = itemcode
        self.hotelsearchcode = hotelsearchcode
        self.roomid = roomid
        self.class = class
        self.tf_supplier = tf_supplier

class Roomtypes(Base):
    __tablename__ = 'roomtypes'
    id = Column(Integer, primary_key=True)
    tb = Column(String)
    db = Column(String)
    q = Column(String)
    sb = Column(String)
    s = Column(String)
    tr = Column(String)
    a = Column(String)
    ns = Column(String)
    infos = relationship('Info', secondary=info_roomtypes)

    def __init__(self, a=None, tr=None, db=None, q=None, s=None, sb=None, ns=None, tb=None):
        self.a = a
        self.tr = tr
        self.db = db
        self.q = q
        self.s = s
        self.sb = sb
        self.ns = ns
        self.tb = tb

class Text(Base):
    __tablename__ = 'text'
    id = Column(Integer, primary_key=True)
    exterior = Column(String)
    restaurant = Column(String)
    rooms = Column(String)
    general = Column(String)
    lobby = Column(String)
    location = Column(String)
    infos = relationship('Info', secondary=info_text)

    def __init__(self, restaurant=None, general=None, location=None, exterior=None, lobby=None, rooms=None):
        self.restaurant = restaurant
        self.general = general
        self.location = location
        self.exterior = exterior
        self.lobby = lobby
        self.rooms = rooms

class Yq(Base):
    __tablename__ = 'yq'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yq)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Postcode(Base):
    __tablename__ = 'postcode'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=per_booking_postcode)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Dateofbirthadult(Base):
    __tablename__ = 'dateofbirthadult'
    id = Column(Integer, primary_key=True)
    isoptional = Column(Boolean)
    per_paxs = relationship('Per_pax', secondary=dateofbirthadult_per_pax)

    def __init__(self, isoptional=None):
        self.isoptional = isoptional

class Baggage_allowance(Base):
    __tablename__ = 'baggage_allowance'
    id = Column(Integer, primary_key=True)
    ods_ists = relationship('Ods_ist', secondary=baggage_allowance_ods_ist)
    prices = relationship('Price', secondary=baggage_allowance_price)
    hrg_ievs = relationship('Hrg_iev', secondary=baggage_allowance_hrg_iev)
    ist_odss = relationship('Ist_ods', secondary=baggage_allowance_ist_ods)
    datas = relationship('Data', secondary=baggage_allowance_data)
    iev_hrgs = relationship('Iev_hrg', secondary=baggage_allowance_iev_hrg)

    def __init__(self, ):

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    points = Column(Integer)
    avg = Column(Float)
    num = Column(Integer)
    ratingss = relationship('Ratings', secondary=ratings_staff)

    def __init__(self, points=None, num=None, avg=None):
        self.points = points
        self.num = num
        self.avg = avg

class Baggageweight(Base):
    __tablename__ = 'baggageweight'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_paxs = relationship('Per_pax', secondary=baggageweight_per_pax)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Taxinfo(Base):
    __tablename__ = 'taxinfo'
    id = Column(Integer, primary_key=True)
    uds = relationship('Ud', secondary=taxinfo_ud)
    yqs = relationship('Yq', secondary=taxinfo_yq)
    iz_s = relationship('Iz_', secondary=iz__taxinfo)
    vls = relationship('Vl', secondary=taxinfo_vl)
    zo_s = relationship('Zo_', secondary=taxinfo_zo_)
    bgs = relationship('Bg', secondary=bg_taxinfo)
    de_s = relationship('De_', secondary=de__taxinfo)
    yrfs = relationship('Yrf', secondary=taxinfo_yrf)
    hbs = relationship('Hb', secondary=hb_taxinfo)
    yks = relationship('Yk', secondary=taxinfo_yk)
    yris = relationship('Yri', secondary=taxinfo_yri)
    ros = relationship('Ro', secondary=ro_taxinfo)
    yqis = relationship('Yqi', secondary=taxinfo_yqi)
    us_s = relationship('Us_', secondary=taxinfo_us_)
    jks = relationship('Jk', secondary=jk_taxinfo)
    fr_s = relationship('Fr_', secondary=fr__taxinfo)
    xfs = relationship('Xf', secondary=taxinfo_xf)
    vvs = relationship('Vv', secondary=taxinfo_vv)
    yqfs = relationship('Yqf', secondary=taxinfo_yqf)
    ses = relationship('Se', secondary=se_taxinfo)
    qhs = relationship('Qh', secondary=qh_taxinfo)
    ca_s = relationship('Ca_', secondary=ca__taxinfo)
    qx_s = relationship('Qx_', secondary=qx__taxinfo)
    ats = relationship('At', secondary=at_taxinfo)
    ra_s = relationship('Ra_', secondary=ra__taxinfo)
    uss = relationship('Us', secondary=taxinfo_us)
    zns = relationship('Zn', secondary=taxinfo_zn)
    zys = relationship('Zy', secondary=taxinfo_zy)
    rns = relationship('Rn', secondary=rn_taxinfo)
    ads = relationship('Ad', secondary=ad_taxinfo)
    uas = relationship('Ua', secondary=taxinfo_ua)
    ycs = relationship('Yc', secondary=taxinfo_yc)
    fes = relationship('Fe', secondary=fe_taxinfo)
    sq_s = relationship('Sq_', secondary=sq__taxinfo)
    xys = relationship('Xy', secondary=taxinfo_xy)
    hus = relationship('Hu', secondary=hu_taxinfo)
    oys = relationship('Oy', secondary=oy_taxinfo)
    it_s = relationship('It_', secondary=it__taxinfo)
    vts = relationship('Vt', secondary=taxinfo_vt)
    rc_s = relationship('Rc_', secondary=rc__taxinfo)
    cjs = relationship('Cj', secondary=cj_taxinfo)
    uxs = relationship('Ux', secondary=taxinfo_ux)
    aps = relationship('Ap', secondary=ap_taxinfo)
    ays = relationship('Ay', secondary=ay_taxinfo)
    trs = relationship('Tr', secondary=taxinfo_tr)
    dcs = relationship('Dc', secondary=dc_taxinfo)
    rd_s = relationship('Rd_', secondary=rd__taxinfo)
    adults = relationship('Adult', secondary=adult_taxinfo)
    mjs = relationship('Mj', secondary=mj_taxinfo)
    ubs = relationship('Ub', secondary=taxinfo_ub)
    aas = relationship('Aa', secondary=aa_taxinfo)
    lb_s = relationship('Lb_', secondary=lb__taxinfo)
    zfs = relationship('Zf', secondary=taxinfo_zf)
    yrs = relationship('Yr', secondary=taxinfo_yr)
    czs = relationship('Cz', secondary=cz_taxinfo)
    vbs = relationship('Vb', secondary=taxinfo_vb)
    aes = relationship('Ae', secondary=ae_taxinfo)
    xas = relationship('Xa', secondary=taxinfo_xa)

    def __init__(self, ):

class _t(Base):
    __tablename__ = '_t'
    id = Column(Integer, primary_key=True)
    fareinforef = Column(String)
    bookingcode = Column(String)
    cabinclass = Column(String)
    fareinfos = relationship('Fareinfo', secondary=_t_fareinfo)

    def __init__(self, cabinclass=None, fareinforef=None, bookingcode=None):
        self.cabinclass = cabinclass
        self.fareinforef = fareinforef
        self.bookingcode = bookingcode

class Tr(Base):
    __tablename__ = 'tr'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_tr)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class It_(Base):
    __tablename__ = 'it_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=it__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    detail = Column(String)
    name = Column(String)
    code = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=itemdetails_location)

    def __init__(self, code=None, name=None, detail=None):
        self.code = code
        self.name = name
        self.detail = detail

class Yk(Base):
    __tablename__ = 'yk'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yk)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Xa(Base):
    __tablename__ = 'xa'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_xa)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Yc(Base):
    __tablename__ = 'yc'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yc)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Dc(Base):
    __tablename__ = 'dc'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=dc_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Ra_(Base):
    __tablename__ = 'ra_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=ra__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Fullcardnamebreakdown(Base):
    __tablename__ = 'fullcardnamebreakdown'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=fullcardnamebreakdown_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Yr(Base):
    __tablename__ = 'yr'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yr)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Qx_(Base):
    __tablename__ = 'qx_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=qx__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Mobilephone(Base):
    __tablename__ = 'mobilephone'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=mobilephone_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Iev_hrg(Base):
    __tablename__ = 'iev_hrg'
    id = Column(Integer, primary_key=True)
    baggage_allowances = relationship('Baggage_allowance', secondary=baggage_allowance_iev_hrg)

    def __init__(self, ):

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=item_itemdetails)

    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name

class Xy(Base):
    __tablename__ = 'xy'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_xy)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Qh(Base):
    __tablename__ = 'qh'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=qh_taxinfo)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Zn(Base):
    __tablename__ = 'zn'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_zn)

    def __init__(self, price=None):
        self.price = price

class Numberofbags(Base):
    __tablename__ = 'numberofbags'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_paxs = relationship('Per_pax', secondary=numberofbags_per_pax)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Farebasis(Base):
    __tablename__ = 'farebasis'
    id = Column(Integer, primary_key=True)
    adults = relationship('Adult', secondary=adult_farebasis)
    detailss = relationship('Details', secondary=details_farebasis)
    prices = relationship('Price', secondary=farebasis_price)

    def __init__(self, ):

class Fareinfo(Base):
    __tablename__ = 'fareinfo'
    id = Column(Integer, primary_key=True)
    _ts = relationship('_t', secondary=_t_fareinfo)
    __ts = relationship('__t', secondary=__t_fareinfo)
    adults = relationship('Adult', secondary=adult_fareinfo)
    prices = relationship('Price', secondary=fareinfo_price)

    def __init__(self, ):

class Zf(Base):
    __tablename__ = 'zf'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_zf)

    def __init__(self, price=None):
        self.price = price

class ____(Base):
    __tablename__ = '____'
    id = Column(Integer, primary_key=True)
    roomid = Column(String)
    itemcode = Column(Integer)
    hotelsearchcode = Column(String)
    gtaitemcode = Column(String)
    hotelcode = Column(Integer)
    id = Column(Integer)
    classid = Column(String)
    class = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=_____itemdetails)
    itemss = relationship('Items', secondary=_____items)
    prices = relationship('Price', secondary=_____price)

    def __init__(self, classid=None, hotelcode=None, gtaitemcode=None, id=None, itemcode=None, hotelsearchcode=None, roomid=None, class=None):
        self.classid = classid
        self.hotelcode = hotelcode
        self.gtaitemcode = gtaitemcode
        self.id = id
        self.itemcode = itemcode
        self.hotelsearchcode = hotelsearchcode
        self.roomid = roomid
        self.class = class

class Baggageallowance(Base):
    __tablename__ = 'baggageallowance'
    id = Column(Integer, primary_key=True)
    numberofpieces = Column(String)
    __ts = relationship('__t', secondary=__t_baggageallowance)

    def __init__(self, numberofpieces=None):
        self.numberofpieces = numberofpieces

class Ticketrules(Base):
    __tablename__ = 'ticketrules'
    id = Column(Integer, primary_key=True)
    refcharge = Column(String)
    minstay = Column(String)
    ticketingfee = Column(Integer)
    original_lasttktdate = Column(String)
    refundable = Column(Boolean)
    maxstay = Column(String)
    lasttktdate = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=itemdetails_ticketrules)

    def __init__(self, ticketingfee=None, lasttktdate=None, refcharge=None, minstay=None, maxstay=None, refundable=None, original_lasttktdate=None):
        self.ticketingfee = ticketingfee
        self.lasttktdate = lasttktdate
        self.refcharge = refcharge
        self.minstay = minstay
        self.maxstay = maxstay
        self.refundable = refundable
        self.original_lasttktdate = original_lasttktdate

class Cardtypes(Base):
    __tablename__ = 'cardtypes'
    id = Column(Integer, primary_key=True)
    _s = relationship('_', secondary=__cardtypes)
    itemdetailss = relationship('Itemdetails', secondary=cardtypes_itemdetails)

    def __init__(self, ):

class Zy(Base):
    __tablename__ = 'zy'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_zy)

    def __init__(self, price=None):
        self.price = price

class Takeoff(Base):
    __tablename__ = 'takeoff'
    id = Column(Integer, primary_key=True)
    max = Column(String)
    min = Column(String)
    rets = relationship('Ret', secondary=ret_takeoff)
    deps = relationship('Dep', secondary=dep_takeoff)

    def __init__(self, max=None, min=None):
        self.max = max
        self.min = min

class Dateofbirthisnotrequiredforadults(Base):
    __tablename__ = 'dateofbirthisnotrequiredforadults'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=dateofbirthisnotrequiredforadults_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Iz_(Base):
    __tablename__ = 'iz_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=iz__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Different_checkin(Base):
    __tablename__ = 'different_checkin'
    id = Column(Integer, primary_key=True)
    checkout = Column(Integer)
    checkin = Column(Integer)
    datas = relationship('Data', secondary=data_different_checkin)

    def __init__(self, checkout=None, checkin=None):
        self.checkout = checkout
        self.checkin = checkin

class Ret(Base):
    __tablename__ = 'ret'
    id = Column(Integer, primary_key=True)
    legsnum = Column(Integer)
    takeoffs = relationship('Takeoff', secondary=ret_takeoff)
    _s = relationship('_', secondary=__ret)
    start_ends = relationship('Start_end', secondary=ret_start_end)
    itemdetailss = relationship('Itemdetails', secondary=itemdetails_ret)
    landings = relationship('Landing', secondary=landing_ret)

    def __init__(self, legsnum=None):
        self.legsnum = legsnum

class Dateofbirth(Base):
    __tablename__ = 'dateofbirth'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_paxs = relationship('Per_pax', secondary=dateofbirth_per_pax)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Waiting(Base):
    __tablename__ = 'waiting'
    id = Column(Integer, primary_key=True)
    max = Column(String)
    min = Column(String)
    ffilters = relationship('Ffilter', secondary=ffilter_waiting)

    def __init__(self, max=None, min=None):
        self.max = max
        self.min = min

class Roomfacility(Base):
    __tablename__ = 'roomfacility'
    id = Column(Integer, primary_key=True)
    _in = Column(String)
    o_ = Column(String)
    _tv = Column(String)
    _vl = Column(String)
    _mb = Column(String)
    _lt = Column(String)
    _sv = Column(String)
    _hd = Column(String)
    _dd = Column(String)
    c_ = Column(String)
    _aw = Column(String)
    _fi = Column(String)
    _ac = Column(String)
    _ra = Column(String)
    _tp = Column(String)
    infos = relationship('Info', secondary=info_roomfacility)

    def __init__(self, _aw=None, _lt=None, _in=None, _tp=None, _dd=None, _vl=None, _ra=None, o_=None, _mb=None, _ac=None, _tv=None, _hd=None, c_=None, _fi=None, _sv=None):
        self._aw = _aw
        self._lt = _lt
        self._in = _in
        self._tp = _tp
        self._dd = _dd
        self._vl = _vl
        self._ra = _ra
        self.o_ = o_
        self._mb = _mb
        self._ac = _ac
        self._tv = _tv
        self._hd = _hd
        self.c_ = c_
        self._fi = _fi
        self._sv = _sv

class Rn(Base):
    __tablename__ = 'rn'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=rn_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Ro(Base):
    __tablename__ = 'ro'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=ro_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Rd_(Base):
    __tablename__ = 'rd_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=rd__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Bg(Base):
    __tablename__ = 'bg'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=bg_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Yri(Base):
    __tablename__ = 'yri'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yri)

    def __init__(self, price=None):
        self.price = price

class Itemfacility(Base):
    __tablename__ = 'itemfacility'
    id = Column(Integer, primary_key=True)
    _bp = Column(String)
    _gf = Column(String)
    _bs = Column(String)
    _hp = Column(String)
    _fl = Column(String)
    _ip = Column(String)
    _te = Column(String)
    _ls = Column(String)
    _pt = Column(String)
    _df = Column(String)
    _ta = Column(String)
    _cr = Column(String)
    _sh = Column(String)
    _gy = Column(String)
    _rs = Column(String)
    _cp = Column(String)
    _sa = Column(String)
    _bc = Column(String)
    _so = Column(String)
    _op = Column(String)
    _kp = Column(String)
    _lf = Column(String)
    _ly = Column(String)
    _bq = Column(String)
    _ec = Column(String)
    infos = relationship('Info', secondary=info_itemfacility)

    def __init__(self, _bs=None, _df=None, _bq=None, _bc=None, _fl=None, _ls=None, _ly=None, _hp=None, _pt=None, _lf=None, _rs=None, _gf=None, _ec=None, _cp=None, _cr=None, _kp=None, _gy=None, _bp=None, _ta=None, _te=None, _sh=None, _op=None, _so=None, _sa=None, _ip=None):
        self._bs = _bs
        self._df = _df
        self._bq = _bq
        self._bc = _bc
        self._fl = _fl
        self._ls = _ls
        self._ly = _ly
        self._hp = _hp
        self._pt = _pt
        self._lf = _lf
        self._rs = _rs
        self._gf = _gf
        self._ec = _ec
        self._cp = _cp
        self._cr = _cr
        self._kp = _kp
        self._gy = _gy
        self._bp = _bp
        self._ta = _ta
        self._te = _te
        self._sh = _sh
        self._op = _op
        self._so = _so
        self._sa = _sa
        self._ip = _ip

class Gmap(Base):
    __tablename__ = 'gmap'
    id = Column(Integer, primary_key=True)
    lng = Column(String)
    lat = Column(String)
    filters = relationship('Filter', secondary=filter_gmap)

    def __init__(self, lat=None, lng=None):
        self.lat = lat
        self.lng = lng

class Svcbreakdown(Base):
    __tablename__ = 'svcbreakdown'
    id = Column(Integer, primary_key=True)
    ____ = Column(Float)
    _ = Column(Integer)
    childs = relationship('Child', secondary=child_svcbreakdown)
    adults = relationship('Adult', secondary=adult_svcbreakdown)

    def __init__(self, ____=None, _=None):
        self.____ = ____
        self._ = _

class Phoneareacode(Base):
    __tablename__ = 'phoneareacode'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=per_booking_phoneareacode)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class ___(Base):
    __tablename__ = '___'
    id = Column(Integer, primary_key=True)
    roomid = Column(String)
    itemcode = Column(String)
    city = Column(String)
    hotelsearchcode = Column(String)
    gtaitemcode = Column(String)
    hotelcode = Column(Integer)
    tf_supplier = Column(String)
    id = Column(Integer)
    classid = Column(String)
    class = Column(String)
    itemss = relationship('Items', secondary=____items)
    prices = relationship('Price', secondary=____price)
    itemdetailss = relationship('Itemdetails', secondary=____itemdetails)

    def __init__(self, classid=None, city=None, hotelcode=None, gtaitemcode=None, id=None, itemcode=None, hotelsearchcode=None, roomid=None, class=None, tf_supplier=None):
        self.classid = classid
        self.city = city
        self.hotelcode = hotelcode
        self.gtaitemcode = gtaitemcode
        self.id = id
        self.itemcode = itemcode
        self.hotelsearchcode = hotelsearchcode
        self.roomid = roomid
        self.class = class
        self.tf_supplier = tf_supplier

class _(Base):
    __tablename__ = '_'
    id = Column(Integer, primary_key=True)
    daychg = Column(Integer)
    equipment = Column(String)
    seats = Column(String)
    elapsedtime = Column(String)
    endpt_name = Column(String)
    flighttime = Column(String)
    baggage_allowance = Column(String)
    technical_stop = Column(String)
    startpt_name = Column(String)
    lcc = Column(String)
    market = Column(String)
    uapi = Column(String)
    class = Column(String)
    startpt_terminal = Column(String)
    roomid = Column(String)
    currency = Column(String)
    date_ = Column(String)
    operating_flightnum = Column(String)
    stops = Column(Integer)
    bookingcode = Column(String)
    starttime = Column(String)
    id = Column(String)
    operating_airv = Column(String)
    gtaitemcode = Column(String)
    hotelcode = Column(Integer)
    endpt = Column(String)
    rbd = Column(String)
    classid = Column(String)
    airvname = Column(String)
    class_name = Column(String)
    code = Column(String)
    segment = Column(String)
    type = Column(String)
    tf_supplier = Column(String)
    legid = Column(String)
    date = Column(String)
    etck = Column(String)
    endpt_terminal = Column(String)
    bic = Column(String)
    key = Column(String)
    plane = Column(String)
    ground_time = Column(String)
    hotelsearchcode = Column(String)
    married_segment = Column(Boolean)
    price = Column(Integer)
    endtime = Column(String)
    availability = Column(String)
    airport_date_change = Column(Integer)
    startpt = Column(String)
    segnum = Column(Integer)
    operating_airvname = Column(String)
    airv = Column(String)
    city = Column(String)
    cabin = Column(String)
    journeytime = Column(String)
    flightnum = Column(String)
    itemcode = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=__itemdetails)
    adults = relationship('Adult', secondary=__adult)
    rets = relationship('Ret', secondary=__ret)
    deps = relationship('Dep', secondary=__dep)
    cardtypess = relationship('Cardtypes', secondary=__cardtypes)
    itemss = relationship('Items', secondary=__items)
    _s = relationship('_', secondary=___)
    prices = relationship('Price', secondary=__price)

    def __init__(self, classid=None, flightnum=None, hotelcode=None, key=None, gtaitemcode=None, airport_date_change=None, legid=None, endpt_terminal=None, code=None, journeytime=None, seats=None, baggage_allowance=None, hotelsearchcode=None, id=None, market=None, flighttime=None, city=None, startpt_terminal=None, class_name=None, operating_airvname=None, stops=None, availability=None, equipment=None, airv=None, startpt=None, etck=None, segnum=None, type=None, cabin=None, operating_flightnum=None, married_segment=None, price=None, bic=None, date_=None, airvname=None, elapsedtime=None, plane=None, lcc=None, startpt_name=None, date=None, technical_stop=None, endtime=None, segment=None, class=None, operating_airv=None, currency=None, daychg=None, bookingcode=None, endpt_name=None, itemcode=None, uapi=None, tf_supplier=None, starttime=None, ground_time=None, rbd=None, roomid=None, endpt=None):
        self.classid = classid
        self.flightnum = flightnum
        self.hotelcode = hotelcode
        self.key = key
        self.gtaitemcode = gtaitemcode
        self.airport_date_change = airport_date_change
        self.legid = legid
        self.endpt_terminal = endpt_terminal
        self.code = code
        self.journeytime = journeytime
        self.seats = seats
        self.baggage_allowance = baggage_allowance
        self.hotelsearchcode = hotelsearchcode
        self.id = id
        self.market = market
        self.flighttime = flighttime
        self.city = city
        self.startpt_terminal = startpt_terminal
        self.class_name = class_name
        self.operating_airvname = operating_airvname
        self.stops = stops
        self.availability = availability
        self.equipment = equipment
        self.airv = airv
        self.startpt = startpt
        self.etck = etck
        self.segnum = segnum
        self.type = type
        self.cabin = cabin
        self.operating_flightnum = operating_flightnum
        self.married_segment = married_segment
        self.price = price
        self.bic = bic
        self.date_ = date_
        self.airvname = airvname
        self.elapsedtime = elapsedtime
        self.plane = plane
        self.lcc = lcc
        self.startpt_name = startpt_name
        self.date = date
        self.technical_stop = technical_stop
        self.endtime = endtime
        self.segment = segment
        self.class = class
        self.operating_airv = operating_airv
        self.currency = currency
        self.daychg = daychg
        self.bookingcode = bookingcode
        self.endpt_name = endpt_name
        self.itemcode = itemcode
        self.uapi = uapi
        self.tf_supplier = tf_supplier
        self.starttime = starttime
        self.ground_time = ground_time
        self.rbd = rbd
        self.roomid = roomid
        self.endpt = endpt

class Geocodes(Base):
    __tablename__ = 'geocodes'
    id = Column(Integer, primary_key=True)
    lon = Column(String)
    lat = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=geocodes_itemdetails)
    infos = relationship('Info', secondary=geocodes_info)

    def __init__(self, latitude=None, lat=None, lon=None, longitude=None):
        self.latitude = latitude
        self.lat = lat
        self.lon = lon
        self.longitude = longitude

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    ____s = relationship('____', secondary=_____items)
    ___s = relationship('___', secondary=____items)
    _s = relationship('_', secondary=__items)
    datas = relationship('Data', secondary=data_items)
    __s = relationship('__', secondary=___items)

    def __init__(self, ):

class Filter(Base):
    __tablename__ = 'filter'
    id = Column(Integer, primary_key=True)
    hotelname = Column(String)
    datas = relationship('Data', secondary=data_filter)
    prices = relationship('Price', secondary=filter_price)
    gmaps = relationship('Gmap', secondary=filter_gmap)
    distances = relationship('Distance', secondary=distance_filter)

    def __init__(self, hotelname=None):
        self.hotelname = hotelname

class __t(Base):
    __tablename__ = '__t'
    id = Column(Integer, primary_key=True)
    endorsement = Column(String)
    departuredate = Column(String)
    destination = Column(String)
    amount = Column(String)
    farerulekey = Column(String)
    bookingcode = Column(String)
    key = Column(String)
    notvalidafter = Column(String)
    notvalidbefore = Column(String)
    farebasis = Column(String)
    origin = Column(String)
    passengertypecode = Column(String)
    fareinforef = Column(String)
    negotiatedfare = Column(String)
    effectivedate = Column(String)
    cabinclass = Column(String)
    fareinfos = relationship('Fareinfo', secondary=__t_fareinfo)
    baggageallowances = relationship('Baggageallowance', secondary=__t_baggageallowance)

    def __init__(self, origin=None, cabinclass=None, passengertypecode=None, effectivedate=None, farebasis=None, destination=None, notvalidbefore=None, negotiatedfare=None, bookingcode=None, notvalidafter=None, amount=None, fareinforef=None, departuredate=None, key=None, endorsement=None, farerulekey=None):
        self.origin = origin
        self.cabinclass = cabinclass
        self.passengertypecode = passengertypecode
        self.effectivedate = effectivedate
        self.farebasis = farebasis
        self.destination = destination
        self.notvalidbefore = notvalidbefore
        self.negotiatedfare = negotiatedfare
        self.bookingcode = bookingcode
        self.notvalidafter = notvalidafter
        self.amount = amount
        self.fareinforef = fareinforef
        self.departuredate = departuredate
        self.key = key
        self.endorsement = endorsement
        self.farerulekey = farerulekey

class Airport(Base):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    ffilters = relationship('Ffilter', secondary=airport_ffilter)

    def __init__(self, ):

class Lccterms(Base):
    __tablename__ = 'lccterms'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    code = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=itemdetails_lccterms)

    def __init__(self, url=None, code=None, name=None):
        self.url = url
        self.code = code
        self.name = name

class Oy(Base):
    __tablename__ = 'oy'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=oy_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Cj(Base):
    __tablename__ = 'cj'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=cj_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Rc_(Base):
    __tablename__ = 'rc_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=rc__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Itemdetails(Base):
    __tablename__ = 'itemdetails'
    id = Column(Integer, primary_key=True)
    stars = Column(Integer)
    gmap_image = Column(String)
    itemtype = Column(Integer)
    checked = Column(Integer)
    ssr = Column(Boolean)
    bestprice = Column(Integer)
    thumbnail = Column(String)
    geocodess = relationship('Geocodes', secondary=geocodes_itemdetails)
    deps = relationship('Dep', secondary=dep_itemdetails)
    _s = relationship('_', secondary=__itemdetails)
    __s = relationship('__', secondary=___itemdetails)
    ____s = relationship('____', secondary=_____itemdetails)
    ratingss = relationship('Ratings', secondary=itemdetails_ratings)
    infos = relationship('Info', secondary=info_itemdetails)
    ___s = relationship('___', secondary=____itemdetails)
    locations = relationship('Location', secondary=itemdetails_location)
    datas = relationship('Data', secondary=data_itemdetails)
    items = relationship('Item', secondary=item_itemdetails)
    citys = relationship('City', secondary=city_itemdetails)
    distances = relationship('Distance', secondary=distance_itemdetails)
    extrainfos = relationship('Extrainfo', secondary=extrainfo_itemdetails)
    rets = relationship('Ret', secondary=itemdetails_ret)
    lcctermss = relationship('Lccterms', secondary=itemdetails_lccterms)
    ticketruless = relationship('Ticketrules', secondary=itemdetails_ticketrules)
    cardtypess = relationship('Cardtypes', secondary=cardtypes_itemdetails)

    def __init__(self, checked=None, itemtype=None, ssr=None, stars=None, bestprice=None, thumbnail=None, gmap_image=None):
        self.checked = checked
        self.itemtype = itemtype
        self.ssr = ssr
        self.stars = stars
        self.bestprice = bestprice
        self.thumbnail = thumbnail
        self.gmap_image = gmap_image

class Childrenandinfantssearch(Base):
    __tablename__ = 'childrenandinfantssearch'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=childrenandinfantssearch_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Xf(Base):
    __tablename__ = 'xf'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_xf)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Cz(Base):
    __tablename__ = 'cz'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=cz_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Prepaycustomersourceidentifier(Base):
    __tablename__ = 'prepaycustomersourceidentifier'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=per_booking_prepaycustomersourceidentifier)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Us_(Base):
    __tablename__ = 'us_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_us_)

    def __init__(self, price=None):
        self.price = price

class Fr_(Base):
    __tablename__ = 'fr_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=fr__taxinfo)

    def __init__(self, price=None):
        self.price = price

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    itemdetailss = relationship('Itemdetails', secondary=city_itemdetails)

    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    points = Column(Integer)
    avg = Column(Float)
    num = Column(Integer)
    ratingss = relationship('Ratings', secondary=ratings_service)

    def __init__(self, points=None, num=None, avg=None):
        self.points = points
        self.num = num
        self.avg = avg

class Yrf(Base):
    __tablename__ = 'yrf'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yrf)

    def __init__(self, price=None):
        self.price = price

class Ux(Base):
    __tablename__ = 'ux'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_ux)

    def __init__(self, price=None):
        self.price = price

class Billingaddress(Base):
    __tablename__ = 'billingaddress'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=billingaddress_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Sort(Base):
    __tablename__ = 'sort'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    order = Column(String)
    datas = relationship('Data', secondary=data_sort)

    def __init__(self, type=None, order=None):
        self.type = type
        self.order = order

class Ca_(Base):
    __tablename__ = 'ca_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=ca__taxinfo)

    def __init__(self, price=None):
        self.price = price

class De_(Base):
    __tablename__ = 'de_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=de__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Childrenandinfantsbooking(Base):
    __tablename__ = 'childrenandinfantsbooking'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=childrenandinfantsbooking_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Landing(Base):
    __tablename__ = 'landing'
    id = Column(Integer, primary_key=True)
    max = Column(String)
    min = Column(String)
    deps = relationship('Dep', secondary=dep_landing)
    rets = relationship('Ret', secondary=landing_ret)

    def __init__(self, max=None, min=None):
        self.max = max
        self.min = min

class Hu(Base):
    __tablename__ = 'hu'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=hu_taxinfo)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Adult(Base):
    __tablename__ = 'adult'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    markupprice = Column(Float)
    baseprice = Column(String)
    discountprice = Column(Integer)
    providercode = Column(String)
    key = Column(String)
    farecalc = Column(String)
    agentsvcfee = Column(Float)
    svcfee = Column(Float)
    num = Column(Integer)
    total = Column(Float)
    tax = Column(Float)
    agentsvcfeed = Column(Integer)
    pricingmethod = Column(String)
    lastticketdate = Column(String)
    eticketability = Column(String)
    farebasiss = relationship('Farebasis', secondary=adult_farebasis)
    originalprices = relationship('Originalprice', secondary=adult_originalprice)
    svcbreakdowns = relationship('Svcbreakdown', secondary=adult_svcbreakdown)
    _s = relationship('_', secondary=__adult)
    detailss = relationship('Details', secondary=adult_details)
    fareinfos = relationship('Fareinfo', secondary=adult_fareinfo)
    taxinfos = relationship('Taxinfo', secondary=adult_taxinfo)

    def __init__(self, svcfee=None, discountprice=None, key=None, tax=None, farecalc=None, eticketability=None, markupprice=None, currency=None, num=None, pricingmethod=None, agentsvcfee=None, baseprice=None, providercode=None, total=None, lastticketdate=None, agentsvcfeed=None):
        self.svcfee = svcfee
        self.discountprice = discountprice
        self.key = key
        self.tax = tax
        self.farecalc = farecalc
        self.eticketability = eticketability
        self.markupprice = markupprice
        self.currency = currency
        self.num = num
        self.pricingmethod = pricingmethod
        self.agentsvcfee = agentsvcfee
        self.baseprice = baseprice
        self.providercode = providercode
        self.total = total
        self.lastticketdate = lastticketdate
        self.agentsvcfeed = agentsvcfeed

class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    markupprice = Column(Float)
    discountprice = Column(Integer)
    svcfee = Column(Integer)
    baseprice = Column(Float)
    num = Column(String)
    total = Column(Float)
    tax = Column(Float)
    svcbreakdowns = relationship('Svcbreakdown', secondary=child_svcbreakdown)
    originalprices = relationship('Originalprice', secondary=child_originalprice)
    detailss = relationship('Details', secondary=child_details)

    def __init__(self, svcfee=None, discountprice=None, tax=None, markupprice=None, currency=None, num=None, baseprice=None, total=None):
        self.svcfee = svcfee
        self.discountprice = discountprice
        self.tax = tax
        self.markupprice = markupprice
        self.currency = currency
        self.num = num
        self.baseprice = baseprice
        self.total = total

class Hb(Base):
    __tablename__ = 'hb'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=hb_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Per_pax(Base):
    __tablename__ = 'per_pax'
    id = Column(Integer, primary_key=True)
    dateofbirthadults = relationship('Dateofbirthadult', secondary=dateofbirthadult_per_pax)
    numberofbagss = relationship('Numberofbags', secondary=numberofbags_per_pax)
    required_parameterss = relationship('Required_parameters', secondary=per_pax_required_parameters)
    baggageweights = relationship('Baggageweight', secondary=baggageweight_per_pax)
    dateofbirths = relationship('Dateofbirth', secondary=dateofbirth_per_pax)

    def __init__(self, ):

class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True)
    itemname = Column(String)
    phone = Column(String)
    itemfacility = Column(String)
    address = Column(String)
    areadetails = Column(Boolean)
    roomfacility = Column(String)
    roomtypes = Column(Boolean)
    category = Column(String)
    stars = Column(String)
    fax = Column(String)
    distance = Column(Float)
    geocodess = relationship('Geocodes', secondary=geocodes_info)
    roomtypess = relationship('Roomtypes', secondary=info_roomtypes)
    itemdetailss = relationship('Itemdetails', secondary=info_itemdetails)
    itemfacilitys = relationship('Itemfacility', secondary=info_itemfacility)
    roomfacilitys = relationship('Roomfacility', secondary=info_roomfacility)
    texts = relationship('Text', secondary=info_text)

    def __init__(self, category=None, distance=None, areadetails=None, roomtypes=None, itemfacility=None, fax=None, roomfacility=None, phone=None, stars=None, address=None, itemname=None):
        self.category = category
        self.distance = distance
        self.areadetails = areadetails
        self.roomtypes = roomtypes
        self.itemfacility = itemfacility
        self.fax = fax
        self.roomfacility = roomfacility
        self.phone = phone
        self.stars = stars
        self.address = address
        self.itemname = itemname

class Distance(Base):
    __tablename__ = 'distance'
    id = Column(Integer, primary_key=True)
    km = Column(Float)
    max = Column(String)
    min = Column(String)
    filters = relationship('Filter', secondary=distance_filter)
    itemdetailss = relationship('Itemdetails', secondary=distance_itemdetails)

    def __init__(self, max=None, km=None, min=None):
        self.max = max
        self.km = km
        self.min = min

class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    points = Column(Integer)
    avg = Column(Float)
    num = Column(Integer)
    ratingss = relationship('Ratings', secondary=ratings_room)

    def __init__(self, points=None, num=None, avg=None):
        self.points = points
        self.num = num
        self.avg = avg

class Dep(Base):
    __tablename__ = 'dep'
    id = Column(Integer, primary_key=True)
    legsnum = Column(Integer)
    itemdetailss = relationship('Itemdetails', secondary=dep_itemdetails)
    landings = relationship('Landing', secondary=dep_landing)
    takeoffs = relationship('Takeoff', secondary=dep_takeoff)
    _s = relationship('_', secondary=__dep)
    start_ends = relationship('Start_end', secondary=dep_start_end)

    def __init__(self, legsnum=None):
        self.legsnum = legsnum

class Us(Base):
    __tablename__ = 'us'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_us)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Mj(Base):
    __tablename__ = 'mj'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=mj_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Ffilter(Base):
    __tablename__ = 'ffilter'
    id = Column(Integer, primary_key=True)
    start_ends = relationship('Start_end', secondary=ffilter_start_end)
    datas = relationship('Data', secondary=data_ffilter)
    airports = relationship('Airport', secondary=airport_ffilter)
    waitings = relationship('Waiting', secondary=ffilter_waiting)
    fprices = relationship('Fprice', secondary=ffilter_fprice)

    def __init__(self, ):

class Error(Base):
    __tablename__ = 'error'
    id = Column(Integer, primary_key=True)
    message = Column(String)
    ______ = Column(String)
    code = Column(String)
    datas = relationship('Data', secondary=data_error)

    def __init__(self, ______=None, code=None, message=None):
        self.______ = ______
        self.code = code
        self.message = message

class Ud(Base):
    __tablename__ = 'ud'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_ud)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Ua(Base):
    __tablename__ = 'ua'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_ua)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Ub(Base):
    __tablename__ = 'ub'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_ub)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Aa(Base):
    __tablename__ = 'aa'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=aa_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Vb(Base):
    __tablename__ = 'vb'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_vb)

    def __init__(self, price=None):
        self.price = price

class Ae(Base):
    __tablename__ = 'ae'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    countrycode = Column(String)
    taxinfos = relationship('Taxinfo', secondary=ae_taxinfo)

    def __init__(self, price=None, countrycode=None):
        self.price = price
        self.countrycode = countrycode

class Ad(Base):
    __tablename__ = 'ad'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    countrycode = Column(String)
    taxinfos = relationship('Taxinfo', secondary=ad_taxinfo)

    def __init__(self, price=None, countrycode=None):
        self.price = price
        self.countrycode = countrycode

class Extrainfo(Base):
    __tablename__ = 'extrainfo'
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    pic = Column(Integer)
    map = Column(Integer)
    itemdetailss = relationship('Itemdetails', secondary=extrainfo_itemdetails)

    def __init__(self, map=None, pic=None, value=None):
        self.map = map
        self.pic = pic
        self.value = value

class Vl(Base):
    __tablename__ = 'vl'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_vl)

    def __init__(self, price=None):
        self.price = price

class Ist_ods(Base):
    __tablename__ = 'ist_ods'
    id = Column(Integer, primary_key=True)
    baggage_allowances = relationship('Baggage_allowance', secondary=baggage_allowance_ist_ods)

    def __init__(self, ):

class Ap(Base):
    __tablename__ = 'ap'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    countrycode = Column(String)
    taxinfos = relationship('Taxinfo', secondary=ap_taxinfo)

    def __init__(self, price=None, countrycode=None):
        self.price = price
        self.countrycode = countrycode

class Start_end(Base):
    __tablename__ = 'start_end'
    id = Column(Integer, primary_key=True)
    ffilters = relationship('Ffilter', secondary=ffilter_start_end)
    rets = relationship('Ret', secondary=ret_start_end)
    deps = relationship('Dep', secondary=dep_start_end)

    def __init__(self, ):

class Vt(Base):
    __tablename__ = 'vt'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_vt)

    def __init__(self, price=None):
        self.price = price

class At(Base):
    __tablename__ = 'at'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=at_taxinfo)

    def __init__(self, price=None):
        self.price = price

class Vv(Base):
    __tablename__ = 'vv'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_vv)

    def __init__(self, price=None):
        self.price = price

class Fprice(Base):
    __tablename__ = 'fprice'
    id = Column(Integer, primary_key=True)
    max = Column(String)
    min = Column(String)
    ffilters = relationship('Ffilter', secondary=ffilter_fprice)

    def __init__(self, max=None, min=None):
        self.max = max
        self.min = min

class Ay(Base):
    __tablename__ = 'ay'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=ay_taxinfo)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Per_booking(Base):
    __tablename__ = 'per_booking'
    id = Column(Integer, primary_key=True)
    dateofbirthisnotrequiredforadultss = relationship('Dateofbirthisnotrequiredforadults', secondary=dateofbirthisnotrequiredforadults_per_booking)
    postcodes = relationship('Postcode', secondary=per_booking_postcode)
    cardsecuritynumbers = relationship('Cardsecuritynumber', secondary=cardsecuritynumber_per_booking)
    prepaycustomersourceidentifiers = relationship('Prepaycustomersourceidentifier', secondary=per_booking_prepaycustomersourceidentifier)
    phonecountrycodes = relationship('Phonecountrycode', secondary=per_booking_phonecountrycode)
    usetfprepays = relationship('Usetfprepay', secondary=per_booking_usetfprepay)
    required_parameterss = relationship('Required_parameters', secondary=per_booking_required_parameters)
    phoneareacodes = relationship('Phoneareacode', secondary=per_booking_phoneareacode)
    childrenandinfantsbookings = relationship('Childrenandinfantsbooking', secondary=childrenandinfantsbooking_per_booking)
    fullcardnamebreakdowns = relationship('Fullcardnamebreakdown', secondary=fullcardnamebreakdown_per_booking)
    billingaddresss = relationship('Billingaddress', secondary=billingaddress_per_booking)
    childrenandinfantssearchs = relationship('Childrenandinfantssearch', secondary=childrenandinfantssearch_per_booking)
    mobilephones = relationship('Mobilephone', secondary=mobilephone_per_booking)

    def __init__(self, ):

class Jk(Base):
    __tablename__ = 'jk'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=jk_taxinfo)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Zo_(Base):
    __tablename__ = 'zo_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_zo_)

    def __init__(self, price=None):
        self.price = price

class Ratings(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    num = Column(Integer)
    avg = Column(Float)
    totalrankings = Column(Integer)
    points = Column(Integer)
    services = relationship('Service', secondary=ratings_service)
    prices = relationship('Price', secondary=price_ratings)
    itemdetailss = relationship('Itemdetails', secondary=itemdetails_ratings)
    rooms = relationship('Room', secondary=ratings_room)
    staffs = relationship('Staff', secondary=ratings_staff)

    def __init__(self, city=None, totalrankings=None, num=None, avg=None, points=None):
        self.city = city
        self.totalrankings = totalrankings
        self.num = num
        self.avg = avg
        self.points = points

class Hrg_iev(Base):
    __tablename__ = 'hrg_iev'
    id = Column(Integer, primary_key=True)
    baggage_allowances = relationship('Baggage_allowance', secondary=baggage_allowance_hrg_iev)

    def __init__(self, ):

class Lb_(Base):
    __tablename__ = 'lb_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=lb__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Phonecountrycode(Base):
    __tablename__ = 'phonecountrycode'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=per_booking_phonecountrycode)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Details(Base):
    __tablename__ = 'details'
    id = Column(Integer, primary_key=True)
    farebasiss = relationship('Farebasis', secondary=details_farebasis)
    prices = relationship('Price', secondary=details_price)
    childs = relationship('Child', secondary=child_details)
    adults = relationship('Adult', secondary=adult_details)

    def __init__(self, ):

class Cardsecuritynumber(Base):
    __tablename__ = 'cardsecuritynumber'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=cardsecuritynumber_per_booking)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional

class Breakdown(Base):
    __tablename__ = 'breakdown'
    id = Column(Integer, primary_key=True)
    ____ = Column(Float)
    prices = relationship('Price', secondary=breakdown_price)

    def __init__(self, ____=None):
        self.____ = ____

class Required_parameters(Base):
    __tablename__ = 'required_parameters'
    id = Column(Integer, primary_key=True)
    datas = relationship('Data', secondary=data_required_parameters)
    per_bookings = relationship('Per_booking', secondary=per_booking_required_parameters)
    per_paxs = relationship('Per_pax', secondary=per_pax_required_parameters)

    def __init__(self, ):

class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True)
    bank_conversion_charge = Column(Float)
    baseprice = Column(Float)
    all_charges = Column(Float)
    servicefee = Column(Float)
    refundable = Column(Boolean)
    sfpd = Column(Boolean)
    min = Column(String)
    fareinforq = Column(Boolean)
    agentsvcfee = Column(Float)
    changepenalty = Column(String)
    currency = Column(String)
    total = Column(Float)
    tax = Column(Float)
    origcurrency = Column(String)
    avg = Column(Float)
    markupprice = Column(Float)
    faretype = Column(String)
    additional_charges = Column(Float)
    key = Column(String)
    num = Column(Integer)
    bank_handling_charge = Column(Float)
    max = Column(String)
    agentnetprice = Column(Float)
    discountprice = Column(Integer)
    platingcarrier = Column(String)
    charges_added = Column(Boolean)
    points = Column(Integer)
    lastticketdate = Column(String)
    itfare = Column(Boolean)
    datas = relationship('Data', secondary=data_price)
    __s = relationship('__', secondary=___price)
    baggage_allowances = relationship('Baggage_allowance', secondary=baggage_allowance_price)
    originalprices = relationship('Originalprice', secondary=originalprice_price)
    ratingss = relationship('Ratings', secondary=price_ratings)
    ___s = relationship('___', secondary=____price)
    farebasiss = relationship('Farebasis', secondary=farebasis_price)
    detailss = relationship('Details', secondary=details_price)
    filters = relationship('Filter', secondary=filter_price)
    ____s = relationship('____', secondary=_____price)
    fareinfos = relationship('Fareinfo', secondary=fareinfo_price)
    breakdowns = relationship('Breakdown', secondary=breakdown_price)
    _s = relationship('_', secondary=__price)

    def __init__(self, tax=None, currency=None, num=None, baseprice=None, platingcarrier=None, total=None, discountprice=None, avg=None, min=None, all_charges=None, fareinforq=None, markupprice=None, itfare=None, agentnetprice=None, refundable=None, lastticketdate=None, origcurrency=None, agentsvcfee=None, sfpd=None, max=None, servicefee=None, key=None, additional_charges=None, changepenalty=None, faretype=None, bank_conversion_charge=None, points=None, bank_handling_charge=None, charges_added=None):
        self.tax = tax
        self.currency = currency
        self.num = num
        self.baseprice = baseprice
        self.platingcarrier = platingcarrier
        self.total = total
        self.discountprice = discountprice
        self.avg = avg
        self.min = min
        self.all_charges = all_charges
        self.fareinforq = fareinforq
        self.markupprice = markupprice
        self.itfare = itfare
        self.agentnetprice = agentnetprice
        self.refundable = refundable
        self.lastticketdate = lastticketdate
        self.origcurrency = origcurrency
        self.agentsvcfee = agentsvcfee
        self.sfpd = sfpd
        self.max = max
        self.servicefee = servicefee
        self.key = key
        self.additional_charges = additional_charges
        self.changepenalty = changepenalty
        self.faretype = faretype
        self.bank_conversion_charge = bank_conversion_charge
        self.points = points
        self.bank_handling_charge = bank_handling_charge
        self.charges_added = charges_added

class Rank_details(Base):
    __tablename__ = 'rank_details'
    id = Column(Integer, primary_key=True)
    price_rate = Column(Float)
    fd_rate = Column(Float)
    sd_rate = Column(Float)
    flight_duration = Column(Integer)
    stay_duration = Column(Integer)
    datas = relationship('Data', secondary=data_rank_details)

    def __init__(self, price_rate=None, fd_rate=None, sd_rate=None, flight_duration=None, stay_duration=None):
        self.price_rate = price_rate
        self.fd_rate = fd_rate
        self.sd_rate = sd_rate
        self.flight_duration = flight_duration
        self.stay_duration = stay_duration

class Fsort(Base):
    __tablename__ = 'fsort'
    id = Column(Integer, primary_key=True)
    type = Column(String)
    order = Column(String)
    datas = relationship('Data', secondary=data_fsort)

    def __init__(self, type=None, order=None):
        self.type = type
        self.order = order

class Fe(Base):
    __tablename__ = 'fe'
    id = Column(Integer, primary_key=True)
    currency = Column(String)
    price = Column(Integer)
    taxinfos = relationship('Taxinfo', secondary=fe_taxinfo)

    def __init__(self, currency=None, price=None):
        self.currency = currency
        self.price = price

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True)
    lowcost = Column(Integer)
    hotelcode = Column(Integer)
    position = Column(String)
    fpage = Column(String)
    start_end = Column(String)
    pinonly = Column(String)
    pintype = Column(String)
    fid = Column(String)
    siteid = Column(String)
    currencytype = Column(String)
    roomid = Column(String)
    session_id = Column(String)
    itemcode = Column(String)
    action = Column(String)
    infoid = Column(String)
    transactionid = Column(String)
    class = Column(String)
    classid = Column(String)
    cataloghash = Column(String)
    hid = Column(String)
    fdisplay = Column(String)
    flightrank = Column(Float)
    uniqueid = Column(String)
    hotelsearchcode = Column(String)
    page = Column(String)
    dep = Column(String)
    id = Column(String)
    type = Column(String)
    error = Column(Boolean)
    ret = Column(String)
    hash = Column(String)
    feature = Column(String)
    responsetime = Column(String)
    display = Column(String)
    city = Column(String)
    tf_supplier = Column(String)
    importance = Column(String)
    timestamp = Column(Integer)
    data = Column(Boolean)
    required_parameterss = relationship('Required_parameters', secondary=data_required_parameters)
    errors = relationship('Error', secondary=data_error)
    prices = relationship('Price', secondary=data_price)
    datas = relationship('Data', secondary=data_data)
    sorts = relationship('Sort', secondary=data_sort)
    ffilters = relationship('Ffilter', secondary=data_ffilter)
    itemdetailss = relationship('Itemdetails', secondary=data_itemdetails)
    itemss = relationship('Items', secondary=data_items)
    filters = relationship('Filter', secondary=data_filter)
    rank_detailss = relationship('Rank_details', secondary=data_rank_details)
    different_checkins = relationship('Different_checkin', secondary=data_different_checkin)
    baggage_allowances = relationship('Baggage_allowance', secondary=baggage_allowance_data)
    fsorts = relationship('Fsort', secondary=data_fsort)
    extrass = relationship('Extras', secondary=data_extras)

    def __init__(self, classid=None, fdisplay=None, hotelcode=None, fpage=None, pintype=None, start_end=None, lowcost=None, hotelsearchcode=None, id=None, city=None, flightrank=None, pinonly=None, feature=None, ret=None, currencytype=None, responsetime=None, type=None, tf_supplier=None, hash=None, fid=None, importance=None, timestamp=None, hid=None, uniqueid=None, transactionid=None, data=None, class=None, dep=None, infoid=None, session_id=None, display=None, itemcode=None, siteid=None, error=None, action=None, position=None, roomid=None, page=None, cataloghash=None):
        self.classid = classid
        self.fdisplay = fdisplay
        self.hotelcode = hotelcode
        self.fpage = fpage
        self.pintype = pintype
        self.start_end = start_end
        self.lowcost = lowcost
        self.hotelsearchcode = hotelsearchcode
        self.id = id
        self.city = city
        self.flightrank = flightrank
        self.pinonly = pinonly
        self.feature = feature
        self.ret = ret
        self.currencytype = currencytype
        self.responsetime = responsetime
        self.type = type
        self.tf_supplier = tf_supplier
        self.hash = hash
        self.fid = fid
        self.importance = importance
        self.timestamp = timestamp
        self.hid = hid
        self.uniqueid = uniqueid
        self.transactionid = transactionid
        self.data = data
        self.class = class
        self.dep = dep
        self.infoid = infoid
        self.session_id = session_id
        self.display = display
        self.itemcode = itemcode
        self.siteid = siteid
        self.error = error
        self.action = action
        self.position = position
        self.roomid = roomid
        self.page = page
        self.cataloghash = cataloghash

class Yqi(Base):
    __tablename__ = 'yqi'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yqi)

    def __init__(self, price=None):
        self.price = price

class Ods_ist(Base):
    __tablename__ = 'ods_ist'
    id = Column(Integer, primary_key=True)
    baggage_allowances = relationship('Baggage_allowance', secondary=baggage_allowance_ods_ist)

    def __init__(self, ):

class Yqf(Base):
    __tablename__ = 'yqf'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=taxinfo_yqf)

    def __init__(self, price=None):
        self.price = price

class Extras(Base):
    __tablename__ = 'extras'
    id = Column(Integer, primary_key=True)
    checkout = Column(String)
    currency = Column(String)
    checkin = Column(String)
    datas = relationship('Data', secondary=data_extras)

    def __init__(self, currency=None, checkout=None, checkin=None):
        self.currency = currency
        self.checkout = checkout
        self.checkin = checkin

class Originalprice(Base):
    __tablename__ = 'originalprice'
    id = Column(Integer, primary_key=True)
    baseprice = Column(Float)
    total = Column(Float)
    tax = Column(Float)
    additional_charges = Column(Float)
    prices = relationship('Price', secondary=originalprice_price)
    adults = relationship('Adult', secondary=adult_originalprice)
    childs = relationship('Child', secondary=child_originalprice)

    def __init__(self, total=None, baseprice=None, tax=None, additional_charges=None):
        self.total = total
        self.baseprice = baseprice
        self.tax = tax
        self.additional_charges = additional_charges

class Sq_(Base):
    __tablename__ = 'sq_'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    taxinfos = relationship('Taxinfo', secondary=sq__taxinfo)

    def __init__(self, price=None):
        self.price = price

class Se(Base):
    __tablename__ = 'se'
    id = Column(Integer, primary_key=True)
    price = Column(String)
    countrycode = Column(String)
    taxinfos = relationship('Taxinfo', secondary=se_taxinfo)

    def __init__(self, price=None, countrycode=None):
        self.price = price
        self.countrycode = countrycode

class Usetfprepay(Base):
    __tablename__ = 'usetfprepay'
    id = Column(Integer, primary_key=True)
    displaytext = Column(String)
    isoptional = Column(Boolean)
    per_bookings = relationship('Per_booking', secondary=per_booking_usetfprepay)

    def __init__(self, displaytext=None, isoptional=None):
        self.displaytext = displaytext
        self.isoptional = isoptional


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

