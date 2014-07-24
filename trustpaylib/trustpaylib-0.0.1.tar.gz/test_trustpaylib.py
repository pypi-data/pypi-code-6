# -*- coding: utf-8 -*-
# vim:fenc=utf-8


import pytest

import trustpaylib

try:
    unicode
    py3 = False
except NameError:
    py3 = True
    unicode = lambda s: s


class TestTrustPayCore:

    secret_key = "abcd1234"
    aid = "9876543210"
    pay_request = trustpaylib.build_pay_request(
        AID=aid,
        AMT="123.45",
        CUR="EUR",
        REF="1234567890",
    )

    def test_validate_request(self):
        pr = trustpaylib.build_pay_request()
        with pytest.raises(ValueError):
            trustpaylib.TrustPay.validate_request(pr)
        trustpaylib.TrustPay.validate_request(self.pay_request)
        pr = trustpaylib.build_pay_request(SIG="SIG")
        with pytest.raises(ValueError):
            trustpaylib.TrustPay.validate_request(pr)

        env = trustpaylib.build_environment(
            aid=self.aid,
            secret_key=self.secret_key,
        )
        tp_client = trustpaylib.TrustPay(env)
        pr = tp_client.sign_request(self.pay_request)
        trustpaylib.TrustPay.validate_request(pr)

        pr = trustpaylib.build_pay_request(
            AID=self.aid,
            AMT="123.45",
            REF="1234567890",
            CUR="GRG",
        )
        with pytest.raises(ValueError):
            trustpaylib.TrustPay.validate_request(pr)

        pr = trustpaylib.build_pay_request(
            AID=self.aid,
            AMT="123.45",
            REF="1234567890",
            CUR="EUR",
            LNG="prd",
        )
        with pytest.raises(ValueError):
            trustpaylib.TrustPay.validate_request(pr)

        pr = trustpaylib.build_pay_request(
            AID=self.aid,
            AMT="123.45",
            REF="1234567890",
            CUR="EUR",
            CNT="tra",
        )
        with pytest.raises(ValueError):
            trustpaylib.TrustPay.validate_request(pr)

        pr = trustpaylib.build_pay_request(
            AID=self.aid,
            AMT="123.4566",
            REF="1234567890",
            CUR="EUR",
            CNT="tra",
        )
        with pytest.raises(ValueError):
            trustpaylib.TrustPay.validate_request(pr)

    def test_cls_creation(self):
        with pytest.raises(ValueError):
            trustpaylib.build_environment(lol='olo')
        assert trustpaylib.build_environment(aid=self.aid)
        pr = trustpaylib.build_pay_request(
            AMT=123.45,
            NURL=None,
        )
        if not py3:
            assert isinstance(pr.AMT, unicode)
        assert pr.NURL is None
        assert pr.RURL is None

    def test_sign_msg(self):
        sign = (
            "DF174E635DABBFF7897A82822521DD7"
            "39AE8CC2F83D65F6448DD2FF991481EA3"
        )
        msg = "".join((
            self.aid,
            self.pay_request.AMT,
            self.pay_request.CUR,
            self.pay_request.REF,
        ))
        sign_message = trustpaylib.sign_message
        assert sign_message(self.secret_key, msg) == sign

        env = trustpaylib.build_environment(
            aid=self.aid,
            secret_key=self.secret_key,
        )
        tp_client = trustpaylib.TrustPay(env)

        assert sign_message(
            self.secret_key,
            tp_client.create_signature_msg(self.pay_request),
        ) == sign
        assert tp_client.pay_request_signature(self.pay_request) == sign

    def test_environment(self):
        env = trustpaylib.build_environment(
            aid=self.aid,
            secret_key=self.secret_key,
        )
        assert env.redirect_url is None
        assert env.aid and env.secret_key
        assert env.api_url == trustpaylib.API_URL
        env = trustpaylib.build_environment(
            aid=self.aid,
            secret_key=self.secret_key,
            api_url="grg prd"
        )
        assert env.api_url == "grg prd"
        env = trustpaylib.build_test_environment(
            aid=self.aid,
            secret_key=self.secret_key,
        )
        assert env.api_url == trustpaylib.TEST_API_URL
        env = trustpaylib.build_test_environment(
            aid=self.aid,
            secret_key=self.secret_key,
            api_url="grg prd"
        )
        assert env.api_url == "grg prd"

    def test_filter_nones(self):
        assert not trustpaylib._filter_dict_nones({'none': None})
        filtered = trustpaylib._filter_dict_nones({
            "none": None,
            "value": "Value",
        })
        assert "none" not in filtered
        assert "value" in filtered

    def test_build_link(self):
        env = trustpaylib.build_environment(
            aid=self.aid,
            secret_key=self.secret_key,
        )
        tp_client = trustpaylib.TrustPay(env)
        assert tp_client.build_link(self.pay_request)
        assert trustpaylib.build_link_for_request(
            env.api_url, self.pay_request)

        client_link = tp_client.build_link(
            self.pay_request,
            sign=False,
        )
        link = trustpaylib.build_link_for_request(
            env.api_url, self.pay_request)
        assert client_link == link

    def test_result_codes(self):
        redirect = trustpaylib.build_redirect(
            RES=1001,
            REF="12345",
            PID="1234",
        )
        assert trustpaylib.TrustPay.get_result_desc_from_redirect(redirect)

        notification = trustpaylib.build_notification(
            RES=1001,
            REF="12345",
        )
        assert len(trustpaylib.TrustPay.get_result_desc_from_notification(
            notification)) == 2

    def test_check_notif_signature(self):
        notification = trustpaylib.build_notification(
            AID=unicode("1234567890"),
            TYP=unicode("CRDT"),
            AMT=unicode("123.45"),
            CUR=unicode("EUR"),
            REF=unicode("9876543210"),
            RES=unicode("0"),
            TID=unicode("11111"),
            OID=unicode("1122334455"),
            TSS=unicode("Y"),
            SIG=unicode(
                "97C92D7A0C0AD99CE5DE55C3597D5ADA"
                "0D423991E2D01938BC0F684244814A37"
            )
        )
        env = trustpaylib.build_environment(
            aid=unicode("1234567890"),
            secret_key=self.secret_key,
        )
        tp_client = trustpaylib.TrustPay(env)
        assert tp_client.check_notification_signature(notification)
