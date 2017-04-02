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

# part of "scale_entity" workflow:
# https://github.com/cloudify-cosmo/cloudify-plugins-common/blob/master/cloudify/plugins/workflows.py
# >>>>>------>>>>>----->>>>>----->>>>>
    if isinstance(delta, basestring):
        try:
            delta = int(delta)
        except ValueError:
            raise ValueError('The delta parameter must be a number. Got: {0}'
                             .format(delta))

    if delta == 0:
        ctx.logger.info('delta parameter is 0, so no scaling will take place.')
        return

    scaling_group = ctx.deployment.scaling_groups.get(scalable_entity_name)
    if scaling_group:
        curr_num_instances = scaling_group['properties']['current_instances']
        planned_num_instances = curr_num_instances + delta
        scale_id = scalable_entity_name
    else:
        node = ctx.get_node(scalable_entity_name)
        if not node:
            raise ValueError("No scalable entity named {0} was found".format(
                scalable_entity_name))
        host_node = node.host_node
        scaled_node = host_node if (scale_compute and host_node) else node
        curr_num_instances = scaled_node.number_of_instances
        planned_num_instances = curr_num_instances + delta
        scale_id = scaled_node.id
# <<<<<------<<<<<-----<<<<<-----<<<<<

    if (delta>0) and (planned_num_instances>max_instances):
        ctx.logger.info('Skipping scale, number of instances would be '
                        'more ({0}) than maximum ({1}).'
                        .format(planned_num_instances, max_instances))

        return
    elif (delta<0) and (planned_num_instances<min_instances):
        ctx.logger.info('Skipping scale, number of instances would be '
                        'less ({0}) than minimum ({1}).'
                        .format(planned_num_instances, min_instances))
        return
    else:
        ctx.logger.info('Proceeding with scale from {0} to {1} instances'
                        .format(curr_num_instances, planned_num_instances))

    return scale_entity(ctx=ctx,
                        scalable_entity_name=scalable_entity_name,
                        delta=delta,
                        scale_compute=scale_compute,
                        ignore_failure=ignore_failure,
                        **kwargs)
