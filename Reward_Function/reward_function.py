import math


class Reward:
    def __init__(self, verbose=False):
        self.first_racingpoint_index = 0  # None
        self.verbose = verbose

    def reward_function(self, params):

        # Import package (needed for heading)
        # import math

        ################## HELPER FUNCTIONS ###################

        def dist_2_points(x1, x2, y1, y2):
            return abs(abs(x1-x2)**2 + abs(y1-y2)**2)**0.5

        def closest_2_racing_points_index(racing_coords, car_coords):

            # Calculate all distances to racing points
            distances = []
            for i in range(len(racing_coords)):
                distance = dist_2_points(x1=racing_coords[i][0], x2=car_coords[0],
                                         y1=racing_coords[i][1], y2=car_coords[1])
                distances.append(distance)

            # Get index of the closest racing point
            closest_index = distances.index(min(distances))

            # Get index of the second closest racing point
            distances_no_closest = distances.copy()
            distances_no_closest[closest_index] = 999
            second_closest_index = distances_no_closest.index(
                min(distances_no_closest))

            return [closest_index, second_closest_index]

        def dist_to_racing_line(closest_coords, second_closest_coords, car_coords):

            # Calculate the distances between 2 closest racing points
            a = abs(dist_2_points(x1=closest_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=closest_coords[1],
                                  y2=second_closest_coords[1]))

            # Distances between car and closest and second closest racing point
            b = abs(dist_2_points(x1=car_coords[0],
                                  x2=closest_coords[0],
                                  y1=car_coords[1],
                                  y2=closest_coords[1]))
            c = abs(dist_2_points(x1=car_coords[0],
                                  x2=second_closest_coords[0],
                                  y1=car_coords[1],
                                  y2=second_closest_coords[1]))

            # Calculate distance between car and racing line (goes through 2 closest racing points)
            # try-except in case a=0 (rare bug in DeepRacer)
            try:
                distance = abs(-(a**4) + 2*(a**2)*(b**2) + 2*(a**2)*(c**2) -
                               (b**4) + 2*(b**2)*(c**2) - (c**4))**0.5 / (2*a)
            except:
                distance = b

            return distance

        # Calculate which one of the closest racing points is the next one and which one the previous one
        def next_prev_racing_point(closest_coords, second_closest_coords, car_coords, heading):

            # Virtually set the car more into the heading direction
            heading_vector = [math.cos(math.radians(
                heading)), math.sin(math.radians(heading))]
            new_car_coords = [car_coords[0]+heading_vector[0],
                              car_coords[1]+heading_vector[1]]

            # Calculate distance from new car coords to 2 closest racing points
            distance_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                        x2=closest_coords[0],
                                                        y1=new_car_coords[1],
                                                        y2=closest_coords[1])
            distance_second_closest_coords_new = dist_2_points(x1=new_car_coords[0],
                                                               x2=second_closest_coords[0],
                                                               y1=new_car_coords[1],
                                                               y2=second_closest_coords[1])

            if distance_closest_coords_new <= distance_second_closest_coords_new:
                next_point_coords = closest_coords
                prev_point_coords = second_closest_coords
            else:
                next_point_coords = second_closest_coords
                prev_point_coords = closest_coords

            return [next_point_coords, prev_point_coords]

        def racing_direction_diff(closest_coords, second_closest_coords, car_coords, heading):

            # Calculate the direction of the center line based on the closest waypoints
            next_point, prev_point = next_prev_racing_point(closest_coords,
                                                            second_closest_coords,
                                                            car_coords,
                                                            heading)

            # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
            track_direction = math.atan2(
                next_point[1] - prev_point[1], next_point[0] - prev_point[0])

            # Convert to degree
            track_direction = math.degrees(track_direction)

            # Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(track_direction - heading)
            if direction_diff > 180:
                direction_diff = 360 - direction_diff

            return direction_diff

        # Gives back indexes that lie between start and end index of a cyclical list
        # (start index is included, end index is not)
        def indexes_cyclical(start, end, array_len):

            if end < start:
                end += array_len

            return [index % array_len for index in range(start, end)]

        # Calculate how long car would take for entire lap, if it continued like it did until now
        def projected_time(first_index, closest_index, step_count, times_list):

            # Calculate how much time has passed since start
            current_actual_time = (step_count-1) / 15

            # Calculate which indexes were already passed
            indexes_traveled = indexes_cyclical(
                first_index, closest_index, len(times_list))

            # Calculate how much time should have passed if car would have followed optimals
            current_expected_time = sum(
                [times_list[i] for i in indexes_traveled])

            # Calculate how long one entire lap takes if car follows optimals
            total_expected_time = sum(times_list)

            # Calculate how long car would take for entire lap, if it continued like it did until now
            try:
                projected_time = (current_actual_time /
                                  current_expected_time) * total_expected_time
            except:
                projected_time = 9999

            return projected_time

        #################### RACING LINE ######################

        # Optimal racing line for the Spain track
        # Each row: [x,y,speed,timeFromPreviousPoint]
        racing_track = [[0.62634, 2.8074, 1.39727, 0.08294],
                        [0.63146, 2.69136, 1.39727, 0.08313],
                        [0.64573, 2.57592, 1.39727, 0.08325],
                        [0.6693, 2.46191, 1.39727, 0.08332],
                        [0.70225, 2.35016, 1.39793, 0.08334],
                        [0.74435, 2.24144, 1.30233, 0.08952],
                        [0.79504, 2.13627, 1.1967, 0.09756],
                        [0.8534, 2.03486, 1.1967, 0.09777],
                        [0.9192, 1.93766, 1.1967, 0.09808],
                        [0.99249, 1.84529, 1.1967, 0.09854],
                        [1.0736, 1.75861, 1.1967, 0.0992],
                        [1.16374, 1.67942, 1.1967, 0.10026],
                        [1.26415, 1.6102, 1.5021, 0.08119],
                        [1.37092, 1.54793, 1.67335, 0.07386],
                        [1.48281, 1.49161, 1.88198, 0.06656],
                        [1.5988, 1.44025, 2.07512, 0.06113],
                        [1.71827, 1.39312, 2.33596, 0.05498],
                        [1.84068, 1.34942, 2.5, 0.05199],
                        [1.96573, 1.30848, 2.5, 0.05263],
                        [2.09321, 1.26959, 2.5, 0.05331],
                        [2.22333, 1.23214, 2.5, 0.05416],
                        [2.35625, 1.19189, 2.5, 0.05555],
                        [2.4887, 1.14987, 2.5, 0.05558],
                        [2.62059, 1.10626, 2.5, 0.05557],
                        [2.75193, 1.0611, 2.5, 0.05555],
                        [2.88273, 1.01446, 2.5, 0.05555],
                        [3.01302, 0.96644, 2.5, 0.05554],
                        [3.14289, 0.91728, 2.5, 0.05555],
                        [3.27245, 0.86725, 2.34643, 0.05919],
                        [3.40179, 0.81664, 2.14705, 0.06469],
                        [3.52534, 0.76803, 1.99968, 0.0664],
                        [3.64883, 0.72099, 1.88636, 0.07005],
                        [3.77225, 0.67658, 1.79873, 0.07292],
                        [3.89566, 0.63577, 1.73281, 0.07501],
                        [4.01913, 0.59935, 1.68666, 0.07632],
                        [4.14273, 0.56803, 1.6591, 0.07686],
                        [4.26652, 0.5424, 1.64913, 0.07666],
                        [4.39051, 0.52303, 1.64913, 0.07609],
                        [4.51466, 0.51041, 1.64913, 0.07567],
                        [4.6389, 0.50498, 1.64913, 0.07541],
                        [4.76312, 0.50709, 1.64913, 0.07534],
                        [4.8872, 0.517, 1.64913, 0.07548],
                        [5.01096, 0.53487, 1.65562, 0.07553],
                        [5.13423, 0.56074, 1.67726, 0.07509],
                        [5.2568, 0.59459, 1.71258, 0.07425],
                        [5.37847, 0.63625, 1.75997, 0.07307],
                        [5.49902, 0.68552, 1.81781, 0.07164],
                        [5.61825, 0.74209, 1.88447, 0.07003],
                        [5.73595, 0.80562, 1.95841, 0.0683],
                        [5.85194, 0.87573, 2.03816, 0.0665],
                        [5.96605, 0.95201, 2.12234, 0.06467],
                        [6.07813, 1.03404, 2.20965, 0.06286],
                        [6.18805, 1.1214, 2.29886, 0.06108],
                        [6.2957, 1.21366, 2.38874, 0.05935],
                        [6.40099, 1.31043, 2.47805, 0.05771],
                        [6.50386, 1.41132, 2.5, 0.05764],
                        [6.60426, 1.51598, 2.5, 0.05801],
                        [6.70214, 1.62407, 2.5, 0.05833],
                        [6.79747, 1.73528, 2.5, 0.05859],
                        [6.89022, 1.84935, 2.5, 0.05881],
                        [6.98037, 1.96604, 2.5, 0.05898],
                        [7.06789, 2.08511, 2.5, 0.05911],
                        [7.15274, 2.20639, 2.5, 0.0592],
                        [7.23487, 2.32968, 2.5, 0.05926],
                        [7.31419, 2.45484, 2.5, 0.05927],
                        [7.39063, 2.58173, 2.5, 0.05925],
                        [7.46407, 2.7102, 2.5, 0.05919],
                        [7.53435, 2.84012, 2.47291, 0.05973],
                        [7.6013, 2.97136, 2.36324, 0.06234],
                        [7.66469, 3.10378, 2.25264, 0.06517],
                        [7.72428, 3.23722, 2.14496, 0.06813],
                        [7.77975, 3.37151, 2.04552, 0.07103],
                        [7.83077, 3.50645, 1.9619, 0.07353],
                        [7.87697, 3.6418, 1.90522, 0.07507],
                        [7.91792, 3.77731, 1.88858, 0.07496],
                        [7.95321, 3.91267, 1.8494, 0.07564],
                        [7.9824, 4.04755, 1.80772, 0.07634],
                        [8.00509, 4.18158, 1.67543, 0.08114],
                        [8.02097, 4.31442, 1.54118, 0.08681],
                        [8.02995, 4.44574, 1.41123, 0.09328],
                        [8.03221, 4.57534, 1.27802, 0.10142],
                        [8.02777, 4.70297, 1.14629, 0.1114],
                        [8.01662, 4.82837, 1.0, 0.1259],
                        [7.99802, 4.95103, 1.0, 0.12406],
                        [7.97105, 5.07025, 1.0, 0.12223],
                        [7.93463, 5.18511, 1.0, 0.12049],
                        [7.88732, 5.29429, 1.0, 0.11899],
                        [7.82726, 5.39584, 1.0, 0.11798],
                        [7.75161, 5.48603, 1.11159, 0.1059],
                        [7.66434, 5.56576, 1.21676, 0.09715],
                        [7.56798, 5.63587, 1.33698, 0.08913],
                        [7.46452, 5.69731, 1.42122, 0.08466],
                        [7.35516, 5.75051, 1.50371, 0.08088],
                        [7.24086, 5.79585, 1.56313, 0.07866],
                        [7.12237, 5.83347, 1.6121, 0.07711],
                        [7.00035, 5.86342, 1.65126, 0.07609],
                        [6.87539, 5.88568, 1.68113, 0.0755],
                        [6.74809, 5.90022, 1.70592, 0.07511],
                        [6.61903, 5.90698, 1.72741, 0.07481],
                        [6.4888, 5.90593, 1.74694, 0.07455],
                        [6.35798, 5.89709, 1.75586, 0.07467],
                        [6.22714, 5.8805, 1.75586, 0.07511],
                        [6.09685, 5.85604, 1.80186, 0.07357],
                        [5.96758, 5.82418, 1.80186, 0.07389],
                        [5.83982, 5.78483, 1.82574, 0.07322],
                        [5.71395, 5.73825, 1.85955, 0.07217],
                        [5.5903, 5.68472, 1.9052, 0.07072],
                        [5.46907, 5.62464, 1.9671, 0.06878],
                        [5.35038, 5.55844, 2.05108, 0.06626],
                        [5.23424, 5.48663, 2.1652, 0.06306],
                        [5.12056, 5.40981, 2.32107, 0.05911],
                        [5.00914, 5.32863, 2.5, 0.05514],
                        [4.89973, 5.24377, 2.5, 0.05538],
                        [4.79201, 5.15593, 2.45112, 0.0567],
                        [4.68576, 5.06561, 2.24857, 0.06202],
                        [4.58079, 4.97316, 2.0831, 0.06715],
                        [4.48082, 4.88243, 1.96125, 0.06884],
                        [4.3796, 4.7942, 1.87697, 0.07154],
                        [4.27684, 4.70907, 1.82611, 0.07307],
                        [4.17225, 4.6277, 1.80653, 0.07336],
                        [4.06554, 4.55072, 1.80653, 0.07284],
                        [3.95644, 4.47878, 1.80653, 0.07234],
                        [3.84475, 4.41244, 1.80653, 0.07191],
                        [3.73031, 4.35215, 1.80653, 0.0716],
                        [3.61306, 4.29823, 1.80653, 0.07144],
                        [3.49301, 4.25081, 1.81793, 0.071],
                        [3.37024, 4.20987, 1.86222, 0.0695],
                        [3.24492, 4.17519, 1.94392, 0.06689],
                        [3.11726, 4.14637, 2.06986, 0.06323],
                        [2.98756, 4.12284, 2.24238, 0.05879],
                        [2.85611, 4.10393, 2.43216, 0.0546],
                        [2.72319, 4.08902, 2.5, 0.0535],
                        [2.58903, 4.07761, 2.45689, 0.0548],
                        [2.45387, 4.06945, 2.25692, 0.06],
                        [2.31818, 4.06426, 2.07663, 0.06539],
                        [2.18532, 4.05625, 1.90257, 0.06996],
                        [2.05434, 4.04515, 1.72418, 0.07624],
                        [1.92525, 4.03072, 1.53015, 0.08489],
                        [1.7982, 4.01267, 1.36907, 0.09374],
                        [1.67349, 3.99052, 1.21821, 0.10397],
                        [1.55151, 3.96372, 1.07012, 0.11671],
                        [1.43274, 3.93163, 1.02891, 0.11957],
                        [1.31783, 3.89345, 1.02891, 0.11768],
                        [1.20781, 3.84796, 1.02891, 0.11571],
                        [1.10389, 3.79392, 1.02891, 0.11383],
                        [1.00783, 3.72983, 1.02891, 0.11223],
                        [0.92249, 3.6538, 1.02891, 0.11109],
                        [0.84978, 3.56631, 1.13536, 0.1002],
                        [0.78832, 3.47061, 1.20876, 0.0941],
                        [0.73744, 3.36858, 1.26738, 0.08996],
                        [0.69672, 3.26166, 1.34505, 0.08506],
                        [0.66544, 3.15118, 1.38395, 0.08297],
                        [0.6434, 3.03808, 1.39727, 0.08247],
                        [0.63046, 2.92322, 1.39727, 0.08273]]

        ################## INPUT PARAMETERS ###################

        # Read all input parameters
        all_wheels_on_track = params['all_wheels_on_track']
        x = params['x']
        y = params['y']
        distance_from_center = params['distance_from_center']
        is_left_of_center = params['is_left_of_center']
        heading = params['heading']
        progress = params['progress']
        steps = params['steps']
        speed = params['speed']
        steering_angle = params['steering_angle']
        track_width = params['track_width']
        waypoints = params['waypoints']
        closest_waypoints = params['closest_waypoints']
        is_offtrack = params['is_offtrack']

        ############### OPTIMAL X,Y,SPEED,TIME ################

        # Get closest indexes for racing line (and distances to all points on racing line)
        closest_index, second_closest_index = closest_2_racing_points_index(
            racing_track, [x, y])

        # Get optimal [x, y, speed, time] for closest and second closest index
        optimals = racing_track[closest_index]
        optimals_second = racing_track[second_closest_index]

        # Save first racingpoint of episode for later
        if self.verbose == True:
            self.first_racingpoint_index = 0  # this is just for testing purposes
        if steps == 1:
            self.first_racingpoint_index = closest_index

        ################ REWARD AND PUNISHMENT ################

        ## Define the default reward ##
        reward = 1

        ## Reward if car goes close to optimal racing line ##
        DISTANCE_MULTIPLE = 1
        dist = dist_to_racing_line(optimals[0:2], optimals_second[0:2], [x, y])
        distance_reward = max(1e-3, 1 - (dist/(track_width*0.5)))
        reward += distance_reward * DISTANCE_MULTIPLE

        ## Reward if speed is close to optimal speed ##
        SPEED_DIFF_NO_REWARD = 1
        SPEED_MULTIPLE = 2
        speed_diff = abs(optimals[2]-speed)
        if speed_diff <= SPEED_DIFF_NO_REWARD:
            # we use quadratic punishment (not linear) bc we're not as confident with the optimal speed
            # so, we do not punish small deviations from optimal speed
            speed_reward = (1 - (speed_diff/(SPEED_DIFF_NO_REWARD))**2)**2
        else:
            speed_reward = 0
        reward += speed_reward * SPEED_MULTIPLE

        # Reward if less steps
        REWARD_PER_STEP_FOR_FASTEST_TIME = 1
        STANDARD_TIME = 37
        FASTEST_TIME = 27
        times_list = [row[3] for row in racing_track]
        projected_time = projected_time(
            self.first_racingpoint_index, closest_index, steps, times_list)
        try:
            steps_prediction = projected_time * 15 + 1
            reward_prediction = max(1e-3, (-REWARD_PER_STEP_FOR_FASTEST_TIME*(FASTEST_TIME) /
                                           (STANDARD_TIME-FASTEST_TIME))*(steps_prediction-(STANDARD_TIME*15+1)))
            steps_reward = min(REWARD_PER_STEP_FOR_FASTEST_TIME,
                               reward_prediction / steps_prediction)
        except:
            steps_reward = 0
        reward += steps_reward

        # Zero reward if obviously wrong direction (e.g. spin)
        direction_diff = racing_direction_diff(
            optimals[0:2], optimals_second[0:2], [x, y], heading)
        if direction_diff > 30:
            reward = 1e-3

        # Zero reward of obviously too slow
        speed_diff_zero = optimals[2]-speed
        if speed_diff_zero > 0.5:
            reward = 1e-3

        ## Incentive for finishing the lap in less steps ##
        # should be adapted to track length and other rewards
        REWARD_FOR_FASTEST_TIME = 1500
        STANDARD_TIME = 37  # seconds (time that is easily done by model)
        FASTEST_TIME = 27  # seconds (best time of 1st place on the track)
        if progress == 100:
            finish_reward = max(1e-3, (-REWARD_FOR_FASTEST_TIME /
                                       (15*(STANDARD_TIME-FASTEST_TIME)))*(steps-STANDARD_TIME*15))
        else:
            finish_reward = 0
        reward += finish_reward

        ## Zero reward if off track ##
        if all_wheels_on_track == False:
            reward = 1e-3

        ####################### VERBOSE #######################

        if self.verbose == True:
            print("Closest index: %i" % closest_index)
            print("Distance to racing line: %f" % dist)
            print("=== Distance reward (w/out multiple): %f ===" %
                  (distance_reward))
            print("Optimal speed: %f" % optimals[2])
            print("Speed difference: %f" % speed_diff)
            print("=== Speed reward (w/out multiple): %f ===" % speed_reward)
            print("Direction difference: %f" % direction_diff)
            print("Predicted time: %f" % projected_time)
            print("=== Steps reward: %f ===" % steps_reward)
            print("=== Finish reward: %f ===" % finish_reward)

        #################### RETURN REWARD ####################

        # Always return a float value
        return float(reward)


reward_object = Reward()  # add parameter verbose=True to get noisy output for testing


def reward_function(params):
    return reward_object.reward_function(params)
