select
from account_info_2019 as ai
INNER JOIN account_apprl_year_2019 as aay on ai.account_num = aay.account_num
INNER JOIN res_detail_2019 as rd on aay.account_num = rd.account_num
where ai.division_cd = 'RES'
limit 1000
;
select ai.account_num, ai.street_num, ai.full_street_name, ai.unit_id, ai.property_city, ai.property_zipcode, aay.tot_val
from account_info_2019 as ai
INNER JOIN account_apprl_year_2019 as aay on ai.account_num = aay.account_num
where ai.account_num = '00000416089000000'
;
select *
from account_info_2019
where lower(owner_name1) like '%nowitzki%'
;
select ai.account_num, concat(street_num, ' ', ai.full_street_name, ' ', ai.unit_id, ' ', ai.property_city, ' ', left(ai.property_zipcode,5))
from account_info_2019 as ai
where ai.division_cd = 'RES'
limit 10
;
select ai.account_num, ai.appraisal_yr, aay.tot_val, aay.prev_mkt_val, CASE WHEN aay.tot_val < aay.prev_mkt_val THEN 'Yes' ELSE 'No' END as Increase,
       street_num, street_half_num, full_street_name, property_city, property_zipcode, deed_txfr_date, hospital_juris_desc, college_juris_desc, city_taxable_val, county_taxable_val, isd_taxable_val, hospital_taxable_val, college_taxable_val, tot_living_area_sf, foundation_typ_desc, heating_typ_desc, ac_typ_desc, ext_wall_desc, roof_typ_desc, num_fireplaces, num_kitchens, num_full_baths, num_half_baths, num_wet_bars, num_bedrooms, sprinkler_sys_ind, pool_ind
        from account_info_2019 as ai
        INNER JOIN account_apprl_year_2019 as aay on ai.account_num = aay.account_num
        INNER JOIN res_detail_2019 as rd on aay.account_num = rd.account_num
        where ai.division_cd = 'RES'
        and aay.taxpayer_rep <> ''
        limit 1000
;
