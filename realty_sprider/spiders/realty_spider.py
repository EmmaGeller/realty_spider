# -*- coding: utf-8 -*-
import json
import logging
import re
import time
import redis
import scrapy
from scrapy.spiders import Rule
from realty_sprider.items import HouseDetail, ProjectDetail, CretDetail, Building, HeZuo, PresaleItems, XssList, XMList,Statistics
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.utils.project import get_project_settings

from realty_sprider.myLinkExtractor import MyLinkExtractor

root_url = 'http://ris.szpl.gov.cn/bol/index.aspx'


class RealtySpider(RedisCrawlSpider):
    name = 'realtySpider'
    redis_key = 'realty:start_urls'
    rules = (
        # Rule(MyLinkExtractor(allow=('housedetail\.aspx\?')), callback='parse_housedetail', follow=True),
        # Rule(MyLinkExtractor(allow=('certdetail.aspx\?')), callback='parse_certdetail', follow=True),
        # Rule(MyLinkExtractor(allow=('projectdetail.aspx\?')), callback='parse_projectdetail', follow=True),
        # Rule(MyLinkExtractor(allow=('building.aspx\?')), callback='parse_building', follow=True),
        # Rule(MyLinkExtractor(allow=('hezuo.aspx\?')), callback='parse_hezuo', follow=True)
    )

    def __init__(self, *a, **kwargs):
        super(RealtySpider, self).__init__(*a, **kwargs)
        settings = get_project_settings()
        self.r1 = redis.Redis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'), db=1,
                              decode_responses=True)
        self.r0 = redis.Redis(host=settings.get('REDIS_HOST'), port=settings.get('REDIS_PORT'), db=0,
                              decode_responses=True)
        self.root_url = 'http://ris.szpl.gov.cn/bol/index.aspx'
        self.form = dict(
            __EVENTTARGET='AspNetPager1',
            __EVENTARGUMENT='1',
            __VIEWSTATE='',
            __VIEWSTATEGENERATOR='248CD702',
            __VIEWSTATEENCRYPTED='',
            __EVENTVALIDATION='',
            tep_name='',
            organ_name='',
            site_address='',
            AspNetPager1_input='0'
        )

    def parse_start_url(self, response):
        global current_page, totalPage
        try:
            if re.match('http://ris.szpl.gov.cn/credit/showcjgs/xssList.aspx', response.url) != None:
                yield  scrapy.Request(url='http://ris.szpl.gov.cn/credit/showcjgs/xssList.aspx',callback=self.parse_xssList)
            if re.match('http://ris.szpl.gov.cn/credit/showcjgs/xmList.aspx', response.url) != None:
                yield scrapy.Request(url=response.url, callback=self.parse_xmList)
            if (re.match('http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx', response.url)) != None:
                td = response.xpath('//*[@id="ctl00_ContentPlaceHolder1_updatepanel1"]/table/tr[2]/td[2]/a')[1:]
                for each in td:
                    href = each.xpath('@href').extract_first()
                    eventTarget = re.findall("javascript:__doPostBack\('(\S+)',''\)", href)[0]
                    self.r1.lpush("event_targets", eventTarget)
                yield scrapy.Request(url=response.url, callback=self.parse_ysfcjgs)
            if (re.match('http://ris.szpl.gov.cn/bol/index.aspx', response.url)) != None:
                current_page = response.xpath('//*[@id="AspNetPager1"]/div[1]/b[1]/text()').extract_first().strip()
                blocks = response.xpath('//tr[@bgcolor="#F5F9FC"]')
                for block in blocks:
                    item = PresaleItems()
                    ids = block.xpath('./td[2]/a/@href').extract_first().strip()
                    id = re.findall('./certdetail.aspx\?id=(\d+)', ids)[0]
                    item['id'] = id
                    item['serial_num'] = block.xpath('./td[1]/text()').extract_first().strip()
                    item['presell_certificate'] = block.xpath('./td[2]/a/text()').extract_first().strip()
                    item['project_name'] = block.xpath('./td[3]/a/text()').extract_first().strip()
                    item['develop_enterprise'] = block.xpath('./td[4]/text()').extract_first().strip()
                    item['area'] = block.xpath('./td[5]/text()').extract_first().strip()
                    item['approval_time'] = block.xpath('./td[6]/text()').extract_first()
                    item['table_name'] = 'realty.presale_items'
                    item['url'] = response.url
                    item['abs_id'] = 'id'
                    item['current_page'] = current_page
                    yield item
                totalPage = response.xpath('//*[@id="AspNetPager1"]/div[1]/b[3]/text()').extract_first()
                if int(totalPage) >= int(current_page) + 1:
                    EVENTARGUMENT = str(int(current_page) + 1)
                    self.form['__EVENTARGUMENT'] = EVENTARGUMENT
                    self.form['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
                    self.form['__EVENTVALIDATION'] = response.xpath(
                        '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
                    self.form['AspNetPager1_input'] = str(int(EVENTARGUMENT) - 1)
                    yield scrapy.FormRequest(url=self.root_url, formdata=self.form, callback=self.parse_start_url,
                                             dont_filter=True)
        except Exception as es:
            logging.error('页面解释出错，当前页为', current_page)
            if int(totalPage) >= int(current_page) + 1:
                self.form['__EVENTARGUMENT'] = str(int(current_page) + 1)
                self.form['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
                self.form['__EVENTVALIDATION'] = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
                self.form['AspNetPager1_input'] = str(int(EVENTARGUMENT) - 1)
                yield scrapy.FormRequest(url=self.root_url, formdata=self.form, callback=self.parse_start_url,
                                         dont_filter=True)

    def parse_certdetail(self, response):
        try:
            trs = response.xpath('//tr[@class="a1"]')[0].xpath('./following-sibling::*')
            item = CretDetail()
            id = re.findall('http://ris.szpl.gov.cn/bol/certdetail.aspx\?id=(\d+)', response.url)[0]
            url = response.url
            item['presell_id'] = id
            item['url'] = url
            item['cert_num'] = trs[0].xpath('./td[2]/text()').extract_first().strip()
            item['project_name'] = trs[0].xpath('./td[4]/text()').extract_first().strip()
            item['developers'] = trs[1].xpath('./td[2]/text()').extract_first().strip()
            item['location'] = trs[1].xpath('./td[4]/text()').extract_first().strip()
            item['building_count'] = trs[2].xpath('./td[2]/text()').extract_first().strip()
            item['plot_num'] = trs[2].xpath('./td[4]/text()').extract_first().strip()
            item['property_certify'] = trs[3].xpath('./td[2]/text()').extract_first().strip()
            item['approved_area'] = trs[3].xpath('./td[4]/text()').extract_first().strip()
            item['land_transfer_contract'] = trs[4].xpath('./td[2]/text()').extract_first().strip()
            item['approved_date'] = trs[4].xpath('./td[4]/text()').extract_first().strip()
            item['licence_date'] = trs[5].xpath('./td[2]/text()').extract_first().strip()
            item['note'] = response.xpath('//tr[@class="a1"][last()]/td[2]/text()').extract_first().strip()
            item['table_name'] = 'realty.certdetail'
            cretUsages = []
            usages_trs = trs.xpath('./td[1][text()="用途"]/..').xpath('./td[2][not(starts-with(text(), "--"))]/..')
            for usage_obj in usages_trs:
                cretUsage = {}
                cretUsage['house_usage'] = usage_obj.xpath('./td[2]/text()').extract_first().strip()
                cretUsage['area'] = usage_obj.xpath('./td[4]/text()').extract_first().strip()
                cretUsage['set_count'] = usage_obj.xpath('./td[6]/text()').extract_first().strip()
                cretUsage['table_name'] = 'realty.using_detail'
                cretUsages.append(cretUsage)
            item['usages'] = json.dumps(cretUsages)
            item['abs_id'] = 'presell_id'
            yield item
        except Exception as e:
            self.r1.lpush("erro_url", response.url)
            logging.info('parse_certdetail出错')
            raise e

    def parse_housedetail(self, response):
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            tables = response.xpath('//table')
            table = tables[2]
            item = HouseDetail()
            item['table_name'] = 'realty.house_detail'
            item['id'] = re.findall('http://ris.szpl.gov.cn/bol/housedetail\.aspx\?id=(\d+)', response.url)[0]
            item['url'] = response.url
            item['building_situation'] = table.xpath('./tr[1]/td[2]/text()').extract_first()
            item['building_num'] = table.xpath('./tr[1]/td[4]/text()').extract_first()
            item['house_type'] = table.xpath('./tr[1]/td[6]/text()').extract_first()
            item['contract_num'] = table.xpath('./tr[2]/td[2]/text()').extract_first()
            item['record_price'] = table.xpath('./tr[2]/td[4]/text()').extract_first()
            item['floor_num'] = table.xpath('./tr[3]/td[2]/text()').extract_first()
            item['house_num'] = table.xpath('./tr[3]/td[4]/text()').extract_first()
            item['house_usage'] = table.xpath('./tr[3]/td[6]/text()').extract_first()
            item['building_area'] = table.xpath('./tr[5]/td[2]/text()').extract_first()
            item['indoor_area'] = table.xpath('./tr[5]/td[4]/text()').extract_first()
            item['assessed_area'] = table.xpath('./tr[5]/td[6]/text()').extract_first()
            item['complete_indoor_area'] = table.xpath('./tr[7]/td[2]/text()').extract_first()
            item['complete_assessed_area'] = table.xpath('./tr[7]/td[4]/text()').extract_first()
            item['complete_building_area'] = table.xpath('./tr[7]/td[6]/text()').extract_first()
            item['timestamp'] = timestamp
            item['abs_id'] = 'id'
            for key in item.keys():
                if (item[key] == None):
                    item[key] = '--'
                elif (isinstance(item[key], str)):
                    item[key] = item[key].strip()
            yield item
        except Exception as e:
            self.r1.lpush("erro_url", response.url)
            logging.info('parse_housedetail出错')
            raise e

    def parse_building(self, response):
        form = dict(
            __EVENTTARGET='imgBt2',
            __EVENTARGUMENT='',
            __VIEWSTATE='',
            __VIEWSTATEGENERATOR='B8ED3096',
            __VIEWSTATEENCRYPTED='',
            __EVENTVALIDATION=''
        )
        try:
            id = re.findall('http://ris.szpl.gov.cn/bol/building.aspx\?id=(\d+)&presellid=(\d+)', response.url)
            url = response.url
            building_num = response.xpath(
                '//div[@id="divShowBranch"]/font[@color="red"]/text()').extract_first().strip()
            status = response.xpath('//td[@class="isblockH"]/a/text()').extract_first().strip()
            update_time = response.xpath(
                '//div[@id = "updatepanel1"]/table[2]/tr/td[3]/text()').extract_first().strip()[
                          -10:]
            trs = response.xpath('//div[@id="updatepanel1"]/table[3]').css('tr.a1')
            for tr in trs:
                item = Building()
                tds = tr.xpath('./td')[1:]
                for td in tds:
                    item['url'] = url
                    item['building_num'] = building_num
                    item['status'] = status
                    item['update_time'] = update_time
                    divs = td.xpath('./div')
                    if divs != None and len(divs) != 0:
                        resu = td.xpath('./div[2]/a/@href').extract_first()
                        if resu != None:
                            house_id = re.findall("housedetail.aspx\?id=(\d+)", resu)[0]
                        else:
                            house_id = 'test'
                        item['house_id'] = house_id
                        item['building_id'] = id[0][0]
                        item['house_num'] = td.xpath('./div[1]/text()').extract_first().strip()
                        house = td.xpath('./div[2]/a/img/@src').extract_first()
                        house_status = re.findall(r'imc/(.*?).gif', house)[0]
                        item['house_status'] = house_status
                        item['presell_id'] = id[0][1]
                        item['table_name'] = 'realty.building'
                        item['abs_id'] = 'house_id'
                        yield item
            form['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
            form['__EVENTVALIDATION'] = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
            yield scrapy.FormRequest(url=response.url, formdata=form, callback=self.parse_building, dont_filter=True)
        except Exception as e:
            self.r1.lpush("erro_url", response.url)
            logging.info('parse_building出错')
            raise e

    def parse_hezuo(self, response):
        try:
            tables = response.xpath('//table[@bgcolor="#99ccff"]')
            presell_id = re.findall('http://ris.szpl.gov.cn/bol/hezuo.aspx\?id=(\d+)', response.url)[0]
            for table in tables:
                item = HeZuo()
                item['url'] = response.url
                item['seller'] = table.xpath('./tr[1]/td[2]/text()').extract_first()
                item['address'] = table.xpath('./tr[2]/td[2]/text()').extract_first()
                item['tel'] = table.xpath('./tr[2]/td[4]/text()').extract_first()
                item['qualify_certification'] = table.xpath('./tr[3]/td[2]/text()').extract_first()
                item['business_license'] = table.xpath('./tr[3]/td[4]/text()').extract_first()
                item['economic_type'] = table.xpath('./tr[4]/td[2]/text()').extract_first()
                item['representative'] = table.xpath('./tr[4]/td[4]/div/text()').extract_first()
                item['representative_nation'] = table.xpath('./tr[5]/td[2]/text()').extract_first()
                item['certificate_type'] = table.xpath('./tr[5]/td[4]/text()').extract_first()
                item['re_id_num'] = table.xpath('./tr[6]/td[2]/text()').extract_first()
                item['principal_agent'] = table.xpath('./tr[7]/td[2]/text()').extract_first()
                item['nation'] = table.xpath('./tr[7]/td[4]/text()').extract_first()
                item['agent_phone_num'] = table.xpath('./tr[8]/td[4]/text()').extract_first()
                item['agent_id_num'] = table.xpath('./tr[8]/td[2]/text()').extract_first()
                item['agent_address'] = table.xpath('./tr[9]/td[2]/text()').extract_first()
                item['table_name'] = 'realty.hezuo'
                item['presell_id'] = presell_id
                for key in item.keys():
                    if (item[key] == None):
                        item[key] = '--'
                    else:
                        item[key] = item[key].strip()
                item['abs_id'] = None
                yield item
        except Exception as e:
            self.r1.lpush("erro_url", response.url)
            logging.info('parse_hezuo出错')
            raise e

    def parse_projectdetail(self, response):
        try:
            table = response.xpath('//table[@bgcolor="#99CCFF"]')
            item = ProjectDetail()
            item['id'] = re.findall('http://ris.szpl.gov.cn/bol/projectdetail.aspx\?id=(\d+)', response.url)[0]
            item['url'] = response.url
            item['project_name'] = table.xpath('./tr[2]/td[2]/text()').extract_first()
            item['zong_num'] = table.xpath('./tr[2]/td[4]/text()').extract_first()
            item['zong_location'] = table.xpath('./tr[3]/td[2]/text()').extract_first()
            item['let_date'] = table.xpath('./tr[4]/td[2]/text()').extract_first()
            item['area'] = table.xpath('./tr[4]/td[4]/text()').extract_first()
            item['ownership_source'] = table.xpath('./tr[5]/td[2]/text()').extract_first()
            item['approval_authority'] = table.xpath('./tr[5]/td[4]/text()/text()').extract_first()
            item['contract_num'] = table.xpath('./tr[6]/td[2]/text()').extract_first()
            item['use_permission'] = table.xpath('./tr[6]/td[4]/text()').extract_first()
            item['supplemental'] = table.xpath('./tr[7]/td[2]/text()').extract_first()
            item['land_use_permit'] = table.xpath('./tr[8]/td[2]/text()').extract_first()
            item['house_using'] = table.xpath('./tr[9]/td[2]/text()').extract_first()
            item['land_using'] = table.xpath('./tr[10]/td[2]/text()').extract_first()
            item['land_grade'] = table.xpath('./tr[10]/td[4]/text()').extract_first()
            item['basic_area'] = table.xpath('./tr[11]/td[2]/text()').extract_first()
            item['zong_area'] = table.xpath('./tr[11]/td[4]/text()').extract_first()
            item['total_area'] = table.xpath('./tr[11]/td[6]/text()').extract_first()
            item['total_presell_set'] = table.xpath('./tr[12]/td[2]/text()').extract_first()
            item['total_presell_area'] = table.xpath('./tr[12]/td[4]/text()').extract_first()
            item['total_sell_cash_area'] = table.xpath('./tr[13]/td[2]/text()').extract_first()
            item['total_sell_cash_set'] = table.xpath('./tr[13]/td[4]/text()').extract_first()
            item['sales_tel_one'] = table.xpath('./tr[14]/td[2]/text()').extract_first()
            item['sales_tel_two'] = table.xpath('./tr[14]/td[4]/text()').extract_first()
            regulatorys = []
            cuor = 15;
            while True:
                regul = {}
                regulatory = table.xpath('./tr[{}]/td[1]/div[1][starts-with(text(), "价款监管机构")]'.format(cuor))
                if regulatory != None and len(regulatory) != 0:
                    regul['price_regulatory'] = table.xpath('./tr[{}]/td[2]/text()'.format(cuor)).extract_first()
                    regul['account_name'] = table.xpath('./tr[{}]/td[2]/text()'.format(cuor + 1)).extract_first()
                    regul['account_num'] = table.xpath('./tr[{}]/td[4]/text()'.format(cuor + 1)).extract_first()
                    regulatorys.append(regul)
                    cuor = cuor + 2
                else:
                    regul['null'] = 'null'
                    break
            item['engineering_regulatory'] = table.xpath('./tr[{}]/td[2]/text()'.format(cuor)).extract_first()
            item['property_management_company'] = table.xpath('./tr[{}]/td[2]/text()'.format(cuor + 1)).extract_first()
            item['management_fee'] = table.xpath('./tr[{}]/td[4]/text()'.format(cuor + 1)).extract_first()
            item['note'] = table.xpath('./tr[{}]/td[4]/text()'.format(cuor + 1)).extract_first()
            trs = table.xpath('// *[ @ id = "DataList1"]/tr[@bgcolor="#F5F9FC"]')
            infos = []
            if len(trs) != 0:
                for tr in trs:
                    info = {}
                    info['project_name'] = tr.xpath('./td[1]/text()').extract_first()
                    info['building_name'] = tr.xpath('./td[2]/text()').extract_first()
                    info['building_permit'] = tr.xpath('./td[3]/text()').extract_first()
                    info['construction_permit'] = tr.xpath('./td[4]/text()').extract_first()
                    infos.append(info)
            else:
                infos = [{'null': 'null'}]
            for key in item.keys():
                if (item[key] == None):
                    item[key] = '--'
                elif (isinstance(item[key], str)):
                    item[key] = item[key].strip()
            item['building_info'] = json.dumps(infos, ensure_ascii=False)
            item['price_regulatory'] = json.dumps(regulatorys, ensure_ascii=False)
            item['table_name'] = 'realty.projectdetail'
            item['abs_id'] = 'id'
            yield item
        except Exception as e:
            self.r1.lpush("erro_url", response.url)
            logging.info('parse_projectdetail出错')
            raise e

    def parse_ysfcjgs(self, response):
        form = dict(
            __EVENTTARGET='',
            __EVENTARGUMENT='',
            __LASTFOCUS='',
            __VIEWSTATE='',
            __VIEWSTATEGENERATOR='',
            __VIEWSTATEENCRYPTED='',
            __EVENTVALIDATION=''
        )
        item = Statistics()
        table1 = {}
        table2 = {}
        list = []
        publish_time = response.xpath('//span[@class="titleblue"]/span/text()').extract_first()
        table = response.xpath('//table[contains(@id,"clientList")]')
        table_1 = table[0]
        trs = table_1.xpath('tr[not(@style)]')[1:]
        area = response.css('a[style="color:Red;"]::text').extract_first()
        for each in trs:
            table1['type'] = each.css('td:first-child::text').extract_first()
            table1['deal_count'] = each.xpath('td[2]/text()').extract_first()
            table1['deal_area'] = each.xpath('td[3]/text()').extract_first()
            table1['price_area'] = each.xpath('td[4]/text()').extract_first()
            table1['available_sale'] = each.xpath('td[5]/text()').extract_first()
            table1['available_area'] = each.xpath('td[6]/text()').extract_first()
            list.append(table1)
        item['huxing_statistics'] = json.dumps(list, ensure_ascii=False)
        table_2 = table[1]
        tr2_list = []
        table2_trs = table_2.xpath('tr')[1:]
        for each in table2_trs:
            table2['area_range'] = each.css('td:first-child::text').extract_first()
            table2['deal_count'] = each.xpath('td[2]/text()').extract_first()
            table2['deal_area'] = each.xpath('td[3]/text()').extract_first()
            table2['price_avg'] = each.xpath('td[4]/text()').extract_first()
            table2['deal_price_count'] = each.xpath('td[5]/text()').extract_first()
            tr2_list.append(table2)
        item['area_statistics'] = json.dumps(tr2_list, ensure_ascii=False)
        table_3 = table[2]
        tr3_list = []
        table3_trs = table_3.xpath('tr')[1:]
        for each in table3_trs:
            table2['using'] = each.css('td:first-child::text').extract_first()
            table2['deal_count'] = each.xpath('td[2]/text()').extract_first()
            table2['deal_area'] = each.xpath('td[3]/text()').extract_first()
            table2['price_avg'] = each.xpath('td[4]/text()').extract_first()
            table2['available_sale'] = each.xpath('td[5]/text()').extract_first()
            table2['available_area'] = each.xpath('td[6]/text()').extract_first()
            tr3_list.append(table1)
        item['using_statistics'] = json.dumps(tr3_list, ensure_ascii=False)
        item['area'] = area
        item['table_name'] = 'realty.statistics'
        item['abs_id'] = None
        item['publish_time'] = publish_time
        yield item
        if (len(self.r1.lrange('event_targets', 0, -1)) != 0):
            eventTarget = self.r1.lpop('event_targets')
            form['__EVENTTARGET'] = eventTarget
            form['__VIEWSTATEGENERATOR'] = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
            form['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
            form['__EVENTVALIDATION'] = response.xpath('//*[@id="__EVENTVALIDATION"]/@value').extract_first()
            yield scrapy.FormRequest(url=response.url, formdata=form, dont_filter=True, callback=self.parse_ysfcjgs)
        else:
            self.r0.lpush('realty:start_urls', 'http://ris.szpl.gov.cn/credit/showcjgs/ysfcjgs.aspx?cjType=1')

    def parse_xmList(self, response):
        global current_page, totalpage
        form = dict(
            __EVENTTARGET='AspNetPager1',
            __EVENTARGUMENT='',
            __VIEWSTATE='',
            __VIEWSTATEGENERATOR='',
            __VIEWSTATEENCRYPTED='',
            __EVENTVALIDATION='',
            drpDistrictList='',
            txtXmName='',
            AspNetPager1_input=''
        )
        try:
            pageinfo = response.xpath('//*[@id="AspNetPager1"]/div[1]/text()').extract_first().strip()
            current_page = re.findall(r'当前为第(\d+)页', pageinfo)[0]
            totalpage = re.findall(r'总共(\d+)页', pageinfo)[0]
            trs = response.xpath('//*[@id="clientList"]/tr')[2:]
            print('current_page=============', current_page)
            for each in trs:
                item = XMList()
                item['serial_num'] = each.xpath('./td[1]/text()').extract_first().strip()
                item['area'] = each.xpath('./td[2]/text()').extract_first().strip()
                item['project_name'] = each.xpath('./td[3]/text()').extract_first().strip()
                item['deal_area'] = each.xpath('./td[4]/text()').extract_first().strip()
                item['deal_set'] = each.xpath('./td[5]/text()').extract_first().strip()
                item['deal_avg_price'] = each.xpath('./td[6]/text()').extract_first().strip()
                item['recall_record'] = each.xpath('./td[7]/text()').extract_first().strip()
                item['table_name'] = 'realty.xmlist'
                item['abs_id'] = None
                yield item
            if int(totalpage) >= int(current_page) + 1:
                EVENTARGUMENT = str(int(current_page) + 1)
                form['__EVENTARGUMENT'] = EVENTARGUMENT
                form['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
                form['__VIEWSTATEGENERATOR'] = response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
                form['__EVENTVALIDATION'] = response.xpath(
                    '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
                form['AspNetPager1_input'] = str(int(EVENTARGUMENT) - 1)
                yield scrapy.FormRequest(url=response.url, formdata=form, callback=self.parse_xmList,
                                         dont_filter=True)
        except Exception as es:
            if int(totalpage) >= int(current_page) + 1:
                EVENTARGUMENT = str(int(current_page) + 1)
                form['__EVENTARGUMENT'] = EVENTARGUMENT
                form['__VIEWSTATE'] = response.xpath('//*[@id="__VIEWSTATE"]/@value').extract_first()
                form['__EVENTVALIDATION'] = response.xpath(
                    '//*[@id="__EVENTVALIDATION"]/@value').extract_first()
                form['AspNetPager1_input'] = str(int(EVENTARGUMENT) - 1)
                yield scrapy.FormRequest(url=response.url, formdata=form, callback=self.parse_xmList,
                                         dont_filter=True)

    def parse_xssList(self,response):
        table = response.xpath('//table[@class="repeater"]')
        trs = table.xpath('./tr')[2:]
        for tr in trs:
            item = XssList()
            item['date'] = tr.xpath('./td[1]/span/text()').extract_first().strip()
            item['area'] = tr.xpath('./td[2]/span/text()').extract_first().strip()
            item['set'] = tr.xpath('./td[3]/span/text()').extract_first().strip()
            item['commodity_set'] = tr.xpath('./td[4]/span/text()').extract_first().strip()
            item['commodity_area'] = tr.xpath('./td[5]/span/text()').extract_first().strip()
            item['table_name'] = 'realty.xsslist'
            item['abs_id'] = None
            yield item
