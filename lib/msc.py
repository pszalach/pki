#!/usr/bin/python3
import logging

from cryptography.x509 import CertificatePolicies, ExtensionNotFound

from lib.utils import binding_from_pem, get_cn


class MSC(object):
    pass

    def __init__(self, pem):
        self.pem = pem
        self.domain_name = ""
        self.chains = []
        self.policy_binding = []

        self._parse(pem)

    def _parse(self, pem):
        certs = pem_to_certs(pem)
        if not certs:
            return
        self.domain_name = get_cn(certs[0])
        self.policy_binding = certs[-1]  # The last cert is a policy binding
        # Parse certificate chains
        chain = []
        for cert in reversed(certs[:-1]):
            chain.insert(0, cert)
            # End of the chain
            if get_cn(cert) == self.domain_name:
                self.chains.insert(0, chain)
                chain = []

    def __str__(self):
        tmp = ["MSC\n"]
        tmp.append("Domain: %s\n" % self.domain_name)
        for chain in self.chains:
            tmp.append("Chain: %s\n" % chain)
        return "".join(tmp)

    def verify(self, trc, scp):
        pass

    def _verify_policy_binding(self):
        pass

    def _verify_policy_binding_integrity(self):
        sep = b'-----BEGIN CERTIFICATE-----\n'
        # Skip the policy binding (the last element)
        pem = sep.join(self.pem.split(sep)[:-1])
        pi, _ = binding_from_pem(pem)
        # Compare with the MSC's policy binding
        try:
            exts = self.policy_binding.extensions.get_extension_for_class(CertificatePolicies)
            return pi == exts.value
        except ExtensionNotFound:
            logging.error("Certificate binding not found.")
            return False


    def _verify_against_trc(self, trc):
        pass

    def _verify_against_proof(self, trc):
        # PSz: needed?
        pass

    def _verify_against_scp(self, scp):
        pass


# Test only
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
# from cryptography.x509 import load_pem_x509_certificate
from lib.utils import pem_to_certs
if __name__ == "__main__":
    with open(sys.argv[1], "rb") as f:
        pem = f.read()
    msc = MSC(pem)
    print(msc)
    print(msc._verify_policy_binding_integrity())
