from scrapy.linkextractors import LinkExtractor
from scrapy.utils.python import unique as unique_list


class MyLinkExtractor(LinkExtractor):
    def extract_links(self, response):
        base_url = 'http://ris.szpl.gov.cn/bol/'
        if self.restrict_xpaths:
            docs = [subdoc
                    for x in self.restrict_xpaths
                    for subdoc in response.xpath(x)]
        else:
            docs = [response.selector]
        all_links = []
        for doc in docs:
            links = self._extract_links(doc, response.url, response.encoding, base_url)
            all_links.extend(self._process_links(links))
        return unique_list(all_links)


