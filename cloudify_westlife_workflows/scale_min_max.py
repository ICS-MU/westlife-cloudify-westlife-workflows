from cloudify import constants, utils
from cloudify.decorators import workflow
from cloudify.plugins import lifecycle
from cloudify.manager import get_rest_client
from cloudify.plugins.workflows import scale_entity

@workflow
def scale_min_max(ctx,
                 scalable_entity_name,
                 delta,
                 scale_compute,
                 ignore_failure=False,
                 **kwargs):
    return scale_entity(ctx=ctx,
                        scalable_entity_name=node_id,
                        delta=delta,
                        scale_compute=scale_compute,
                        **kwargs)
