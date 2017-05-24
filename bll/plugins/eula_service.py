# (c) Copyright 2016-2017 Hewlett Packard Enterprise Development LP
# (c) Copyright 2017 SUSE LLC

import pecan
import pymysql.cursors
from bll.plugins import service


class EulaSvc(service.SvcBase):
    """
    Implements functions for managing the user acceptance of the EULA (End
    User License Agreement)`

    By default the EULA is considered to be accepted, which is due to the fact
    that the user normally has to accept the EULA as part of the install
    process, which has already taken place before the Operations Console is
    running.

    The one scenario where the EULA would be false when the BLL starts is
    when CloudSystem is installed by HPE when in the factory, and when the
    user launches the operations console, they would not have seen it yet.
    For this reason, the factory needs to be able to make a rest call (with
    curl) to explicitly set the accepted status to False.

    The ``target`` value for this plugin is ``eula``. See :ref:`rest-api`
    for a full description of the request and response formats.
    """

    def __init__(self, *args, **kwargs):
        super(EulaSvc, self).__init__(*args, **kwargs)
        config = pecan.conf.db.to_dict()
        config['cursorclass'] = pymysql.cursors.DictCursor
        self.connection = pymysql.connect(**config)

    @service.expose('get_eula_accepted')
    def get(self):
        """
        Returns a boolean indicating whether the EULA has been accepted.
        Defaults to True.

        Request format::

            "target": "eula",
            "operation": "get_eula_accepted"

        """
        # By default, consider the EULA to have been accepted
        accepted = True
        with self.connection.cursor() as cursor:
            sql = "SELECT `accepted` from `eula`"
            cursor.execute(sql)
            row = cursor.fetchone()
            cursor.close()
            if row is not None:
                # Mysql stores the boolean as a 1 or 0, so convert
                # to appropriate python type
                accepted = row.get("accepted") != 0

        return accepted

    @service.expose('put_eula_accepted')
    def put(self):
        """
        Update the EULA accepted status to the given boolean value

        Request format::

            "target": "eula",
            "operation": "put_eula_accepted",
            "eula-accepted": true
        """

        accepted = self.data.get('eula-accepted', True)

        with self.connection.cursor() as cursor:
            sql = "select count(*) from `eula`"
            cursor.execute(sql)
            found = (cursor.fetchone()['count(*)'] == 1)
            if found:
                sql = "UPDATE `eula` SET `accepted`=%s"
            else:
                sql = "INSERT INTO `eula` VALUES (%s)"

            cursor.execute(sql, accepted)
            cursor.close()
        self.connection.commit()

        return {'eula-accepted': accepted}
