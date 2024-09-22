from api.api import API
class PostAW():
    def getCdMicrioserviceApi(self, productId, micrioserviceName):
        """创建AW-自动生成API:获取yaml文档有哪些未生成AW"""
        method = 'GET'
        uri = f'/msa/getCdMicrioserviceApi'
        body = {"productId":productId,"micrioserviceName":micrioserviceName,"branch":self.branch}
        return API(self.host, method, self.headers, uri, body).send_request()

    def createApiDesignAw(self, apiList):
        """创建AW-自动生成API:生成AW"""
        method = 'POST'
        uri = f'/msa/createApiDesignAw'
        body = {"apiList":apiList,"baseUrl":"",,"nameRule":"summary"}
        return API(self.host, method, self.headers, uri, body).send_request()