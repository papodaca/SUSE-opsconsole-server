# (c) Copyright 2016 Hewlett Packard Enterprise Development LP
import pecan
import pymysql.cursors
from tests.util import functional, TestCase
from bll import api
from bll.plugins.eula_service import EulaSvc
from bll.api.request import BllRequest


@functional('mysql')
class TestEula(TestCase):

    def test_get_set_eula(self):

        # Clear out the table before starting the test
        config = pecan.conf.db.to_dict()
        config['cursorclass'] = pymysql.cursors.DictCursor
        connection = pymysql.connect(**config)
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM `eula`")
            cursor.close()
        connection.commit()

        request = {
            'target': 'eula',
            'data': {'operation': 'get_eula_accepted'}
        }

        svc = EulaSvc(bll_request=BllRequest(request))
        reply = svc.handle()
        self.assertEqual('complete', reply[api.STATUS])
        self.assertTrue(reply[api.DATA])

        # Set to False and verify
        request['data']['operation'] = 'put_eula_accepted'
        request['data']['eula-accepted'] = False
        svc = EulaSvc(bll_request=BllRequest(request))
        reply = svc.handle()
        self.assertEqual('complete', reply[api.STATUS])

        request['data']['operation'] = 'get_eula_accepted'
        svc = EulaSvc(bll_request=BllRequest(request))
        reply = svc.handle()
        self.assertEqual('complete', reply[api.STATUS])
        self.assertFalse(reply[api.DATA])

        # Set to True and verify
        request['data']['operation'] = 'put_eula_accepted'
        request['data']['eula-accepted'] = True
        svc = EulaSvc(bll_request=BllRequest(request))
        reply = svc.handle()
        self.assertEqual('complete', reply[api.STATUS])

        request['data']['operation'] = 'get_eula_accepted'
        svc = EulaSvc(bll_request=BllRequest(request))
        reply = svc.handle()
        self.assertEqual('complete', reply[api.STATUS])
        self.assertTrue(reply[api.DATA])
