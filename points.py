import tensorflow as tf
import posenet


def getPoints(cap):
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(101, sess)
        output_stride = model_cfg['output_stride']
        input_image, display_image, output_scale = posenet.read_cap(
            cap, scale_factor=0.7125, output_stride=output_stride)


        heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
            model_outputs,
            feed_dict={'image:0': input_image}
        )

        pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
            heatmaps_result.squeeze(axis=0),
            offsets_result.squeeze(axis=0),
            displacement_fwd_result.squeeze(axis=0),
            displacement_bwd_result.squeeze(axis=0),
            output_stride=output_stride,
            max_pose_detections=10,
            min_pose_score=0.15)

        # Tobillo derecho
        td_y = keypoint_coords[0][16][0]
        td_x = keypoint_coords[0][16][1]
        tobillo_d = (td_x, td_y)  # Punto f (Tobillo)
        # Tobillo izquierdo
        ti_y = keypoint_coords[0][15][0]
        ti_x = keypoint_coords[0][15][1]
        tobillo_i = (ti_x, ti_y)  # Punto f (Tobillo)

        ptTobillos_y = (ti_y + td_y) / 2
        ptTobillos_x = (ti_x + td_x) / 2
        return (ptTobillos_x, ptTobillos_y)
