# Copyright 2017 ETH Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging

from pki.lib.defines import FailCase, SecLevel
from pki.lib.x509 import get_cn


class VrfyResults(object):
    """
    Helper class for storing results of a successful chain verification.
    """
    def __init__(self, chain):
        self.ca = get_cn(chain[-1])
        self.path_len = len(chain)
        # TODO(PSz): derive the following
        self.sec_lvl = SecLevel.MEDIUM
        self.ev = False
        self.valid_for = 12345
        self.wildcard = False

    def __repr__(self):
        s = "<VrfyResult: "
        s += "CA: %s, PathLen: %d, SecLvl: %s, EV: %s, ValidFor: %d, Wildcard: %s" %  (self.ca,
            self.path_len, self.sec_lvl, self.ev, self.valid_for, self.wildcard)
        s += ">"
        return s


class Verifier(object):
    """
    Certificate verifier.
    """

    def __init__(self, domain_name, msc, scp, proof, trc):
        self.domain_name = domain_name
        self.msc = msc
        self.scp = scp
        self.proof = proof
        # TRC's part
        self.trc = trc
        self.trusted_certs = []
        self.trusted_logs = {}
        self.threshold = None
        self._process_trc(trc)

    def _process_trc(self, trc):
        # TODO(PSz): set parameters
        pass

    def verify(self):
        """
        Returns either (True, None) or (False, FailCase.SOFT) or (False, FailCase.HARD)
        """
        # First verify proofs
        if not self._verify_proof():
            return (False, FailCase.HARD)
        if not self._verify_scp():
            return (False, FailCase.HARD)
        return self._verify_msc()


        # return (False, FailCase.SOFT)
        # return (False, FailCase.HARD)
        return (True, None)

    def _verify_proof(self):
        """
        Verify whether the proof is fresh and matches the MSC and SCP.
        """
        return True

    def _verify_scp(self):
        """
        Verify whether SCP matches the TRC (trusted CAs and threshold number).
        """
        return True

    def _verify_msc(self):
        """
        Verify whether MSC matches the SCP and domain name.
        """
        # return (False, FailCase.SOFT)
        # return (False, FailCase.HARD)
        return (True, None)
