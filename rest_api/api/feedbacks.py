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
# ------------------------------------------------------------------------------

from uuid import uuid4
from urllib.parse import unquote

from sanic import Blueprint
from sanic import response

from api.authorization import authorized
from api import common
from api import messaging

from db import feedbacks_query

from marketplace_transaction import transaction_creation


FEEDBACKS_BP = Blueprint('feedbacks')


@FEEDBACKS_BP.post('feedbacks')
@authorized()
async def create_feedback(request):
    """Creates a new Feedbacks in state"""
    required_fields = ['asset', 'rating']
    common.validate_fields(required_fields, request.json)

    feedback = _create_feedback_dict(request)
    signer = await common.get_signer(request)

    batches, batch_id = transaction_creation.create_feedback(
        txn_key=signer,
        batch_key=request.app.config.SIGNER,
        identifier=feedback['id'],
        asset=feedback.get('asset'),
        text=feedback.get('text'),
        rating=feedback.get('rating'))

    await messaging.send(
        request.app.config.VAL_CONN,
        request.app.config.TIMEOUT,
        batches)

    await messaging.check_batch_status(request.app.config.VAL_CONN, batch_id)

    return response.json(feedback)


@FEEDBACKS_BP.get('feedbacks')
async def get_all_feedbacks(request):
    """Fetches complete details of all Feedbacks in state"""
    feedback_resources = await feedbacks_query.fetch_all_feedback_resources(
        request.app.config.DB_CONN)
    return response.json(feedback_resources)


@FEEDBACKS_BP.get('feedbacks/<asset>')
async def get_feedback(request, asset):
    """Fetches the Feedbacks for particular Asset in state"""
    decoded_asset = unquote(asset)
    feedback_resource = await feedbacks_query.fetch_feedback_resource(
        request.app.config.DB_CONN, decoded_asset)
    return response.json(feedback_resource)


def _create_feedback_dict(request):
    keys = ['asset', 'text', 'rating']
    body = request.json

    feedback = {k: body[k] for k in keys if body.get(k) is not None}

    if feedback.get('rating') is None:
        feedback['rating'] = 0

    feedback['id'] = str(uuid4())

    return feedback
