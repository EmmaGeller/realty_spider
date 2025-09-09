# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Building(Item):
    url = Field()
    house_id = Field()
    building_id = Field()
    building_num = Field()
    house_num = Field()
    floor_num = Field()
    status = Field()
    house_status = Field()
    update_time = Field()
    presell_id = Field()
    timestamp = Field()
    table_name=Field()
    abs_id=Field()


# 预售证详情
class CretDetail(Item):
    presell_id = Field()
    url = Field()
    cert_num = Field()  # '许可证号',
    project_name = Field()  # '项目名称',
    developers = Field()  # '发展商',
    location = Field()  # '所在位置',
    building_count = Field()  # '栋数',
    plot_num = Field()  # '地块编号',
    property_certify = Field()  # '房产证编号',
    approved_area = Field()  # '批准面积',
    land_transfer_contract = Field()  # '土地出让合同',
    approved_date = Field()  # '批准日期	',
    licence_date = Field()  # '发证日期',
    using_details = Field()  # '用途',
    note = Field()  # '备注',
    usages=Field()
    table_name=Field()
    abs_id=Field()


class HeZuo(Item):
    presell_id = Field()
    url = Field()
    seller = Field()  # '卖方',
    address = Field()  # '地址',
    tel = Field()  # '电话',
    qualify_certification = Field()  # '开发企业资质证书号码',
    business_license = Field()  # '营业执照号码',
    economic_type = Field()  # '经济类型',
    representative = Field()  # '法定代表人',
    representative_nation = Field()  # '法人国籍',
    certificate_type = Field()  # '证件类型',
    re_id_num = Field()  # '法人身份证/护照号',
    principal_agent = Field()  # '委托代理人',
    nation = Field()  # '委托代理人国籍',
    agent_phone_num = Field()  # '委托代理人电话',
    agent_id_num = Field()  # '委托代理人身份证/护照号',
    agent_address = Field()  # '委托代理人地址',
    table_name=Field()
    abs_id=Field()


class HouseDetail(Item):
    id = Field()
    url = Field()
    building_situation = Field()  # '项目楼栋情况	',
    building_num = Field()  # '座号',
    contract_num = Field()  # '合同号',
    record_price = Field()  # '备案价格',
    floor_num = Field()  # '层号',
    house_num = Field()  # '房号',
    house_usage = Field()  # '用途',
    building_area = Field()  # '建筑面积',
    indoor_area = Field()  # '户内面积	',
    assessed_area = Field()  # '分摊面积',
    complete_indoor_area = Field()  # '竣工户内面积	',
    complete_assessed_area = Field()  # '竣工分摊面积',
    complete_building_area = Field()  # '竣工建筑面积',
    house_type = Field()  # '户型',
    timestamp = Field()
    table_name=Field()
    abs_id=Field()


# '预售项目列表';
class PresaleItems(Item):
    id = Field()
    presell_certificate = Field()  # '预售证号',
    project_name = Field()  # '项目名称',
    develop_enterprise = Field()  # '开发企业',
    area = Field()  # '所在区',
    approval_time = Field()  # '批准时间',
    serial_num = Field()
    url=Field()
    table_name=Field()
    abs_id=Field()
    current_page=Field()


class ProjectDetail(Item):
    id = Field()  #
    url = Field()  #
    zong_num = Field()  # '宗地号',
    project_name = Field()  # '项目名称',
    zong_location = Field()  # '宗地位置',
    let_date = Field()  # '受让日期',
    area = Field()  # '所在区域',
    ownership_source = Field()  # '权属来源',
    approval_authority = Field()  # '批准机关',
    contract_num = Field()  # '合同文号',
    use_permission = Field()  # '使用权限',
    supplemental = Field()  # '补充协议',
    land_use_permit = Field()  # '用地规划许可证',
    house_using = Field()  # '房屋用途',
    land_using = Field()  # '土地用途',
    land_grade = Field()  # '土地等级',
    basic_area = Field()  # '基地面积',
    zong_area = Field()  # '宗地面积',
    total_area = Field()  # '总建筑面积',
    total_presell_set = Field()  # '预售总套数',
    total_presell_area = Field()  # '预售总面积',
    total_sell_cash_area = Field()  # '现售总面积',
    total_sell_cash_set = Field()  # '现售总套数',
    sales_tel_one = Field()  # '售楼电话',
    engineering_regulatory = Field()  # '工程监管机构',
    property_management_company = Field()  # v '物业管理公司',
    management_fee = Field()  # '管理费',
    note = Field()  # '备注',
    sales_tel_two = Field()  #
    price_regulatory=Field()
    building_info=Field()
    table_name=Field()
    abs_id=Field()



class CrawUrls(Item):
    url = Field()
    table_type=Field()
    table_name=Field()
    abs_id=Field()


class XMList(Item):
    serial_num=Field()
    area=Field()
    project_name=Field()
    deal_area=Field()
    deal_set=Field()
    deal_avg_price=Field()
    recall_record=Field()
    table_name=Field()
    abs_id=Field()


class XssList(Item):
    date=Field()
    area=Field()
    set=Field()
    area=Field()
    commodity_set=Field()
    commodity_area=Field()
    table_name=Field()
    abs_id=Field()

class Statistics(Item):
    publish_time=Field()
    huxing_statistics=Field()
    area_statistics=Field()
    using_statistics=Field()
    area=Field()
    table_name=Field()
    abs_id=Field()





