# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

from sawtooth_sdk.processor.exceptions import InvalidTransaction


def handle_feedback_creation(create_feedback, header, state):
    """Handles creating a Feedback.

    Args:
        create_feedback (CreateFeedback): The transaction.
        header (TransactionHeader): The header of the Transaction.
        state (MarketplaceState): The wrapper around the context.

    Raises:
        InvalidTransaction
            - The feedback already exists for this Asset from this account.
            - The txn signer has no account
    """

    if state.get_feedback(identifier=create_feedback.id):
        raise InvalidTransaction("Failed to create Feedback, id {} already "
                                 "exists.".format(create_feedback.id))

    if not state.get_account(public_key=header.signer_public_key):
        raise InvalidTransaction(
            "Unable to create feedback, signing key has no"
            " Account: {}".format(header.signer_public_key))



    # if state.get_feedback(asset=create_feedback.asset):
    #     raise InvalidTransaction(
    #         "Asset already exists with Name {}".format(create_feedback.asset))

    state.set_feedback(
        identifier=create_feedback.id,
        account=header.signer_public_key,
        asset=create_feedback.asset,
        text=create_feedback.text,
        rating=create_feedback.rating)
