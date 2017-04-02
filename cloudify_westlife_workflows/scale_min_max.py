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
                 min_instances,
                 max_instances,
                 ignore_failure=False,
                 **kwargs):
    graph = ctx.graph_mode()
    node = ctx.get_node(scalable_entity_name)
    if not node:
        raise ValueError("Node {0} doesn't exist".format(scalable_entity_name))
    if delta == 0:
        ctx.logger.info('delta parameter is 0, so no scaling will take place.')
        return
    host_node = node.host_node
    scaled_node = host_node if (scale_compute and host_node) else node
    instances_count = scaled_node.number_of_instances
    ctx.logger.info("Current number of instances {0}".format(instances_count))

    return scale_entity(ctx=ctx,
                        scalable_entity_name=scalable_entity_name,
                        delta=delta,
                        scale_compute=scale_compute,
                        ignore_failure=ignore_failure,
                        **kwargs)
