import relationships
import services
import sims4
import sims4.commands
import os.path

GL_FRIENDSHIP_DECAY = 100
GL_ROMANCE_DECAY = 100


filename = os.path.dirname(os.path.realpath(__file__)) + "\\blablabla.cfg"

my_file = open(filename, 'r')
if my_file is not None:
	decay = my_file.read().split()
	if decay:
		GL_FRIENDSHIP_DECAY = decay[0]
		GL_ROMANCE_DECAY = decay[1]

my_file.close()

@sims4.commands.Command('friendship.decay', command_type=sims4.commands.CommandType.Live)
def set_friendship_decay(friendship:int=None, _connection=None):
	output = sims4.commands.CheatOutput(_connection)
	if friendship is not None:
		if friendship >= 0:
			all_sims = services.sim_info_manager().get_all()
			GL_FRIENDSHIP_DECAY = friendship
			modpct = friendship / 100
			output("Working...")
			for sim_info in all_sims:
				relationships = sim_info.relationship_tracker
				for relationship in relationships:
					target_id = relationship.target_sim_id
					target_sim = services.sim_info_manager().get(target_id)
					tracks = sim_info.relationship_tracker.relationship_tracks_gen(target_id)
					for track in tracks:
						if track.stat_type == track.FRIENDSHIP_TRACK:
							decay = track.get_decay_rate_modifier()
							if decay > modpct:
								track.remove_decay_rate_modifier(decay)
								track.add_decay_rate_modifier(modpct)
			output("Done!")
		else:
			output("You have typed in a negative value! Don't type negative values or I'll personally send ninjas after you.")
	else:
		output("Usage: friendship.decay [percentage]")

@sims4.commands.Command('romance.decay', command_type=sims4.commands.CommandType.Live)
def set_romance_decay(romance:int=None, _connection=None):
	output = sims4.commands.CheatOutput(_connection)
	if romance is not None:
		if romance >= 0:
			all_sims = services.sim_info_manager().get_all()
			GL_ROMANCE_DECAY = romance
			modpct = romance / 100
			output("Working...")
			for sim_info in all_sims:
				relationships = sim_info.relationship_tracker
				for relationship in relationships:
					target_id = relationship.target_sim_id
					target_sim = services.sim_info_manager().get(target_id)
					tracks = sim_info.relationship_tracker.relationship_tracks_gen(target_id)
					for track in tracks:
						if track.stat_type == track.ROMANCE_TRACK:
							decay = track.get_decay_rate_modifier()
							if decay > modpct:
								track.remove_decay_rate_modifier(decay)
								track.add_decay_rate_modifier(modpct)
			output("Done!")
		else:
			output("You have typed in a negative value! Don't type negative values or I'll personally send ninjas after you.")
	else:
		output("Usage: romance.decay [percentage]")
					
	

@sims4.commands.Command('showreldecay', command_type=sims4.commands.CommandType.Live)
def doit(_connection=None):
	output = sims4.commands.CheatOutput(_connection)
	active_sim_info = services.client_manager().get(_connection).active_sim
	output('Working...')
	household = active_sim_info.household
	for sim_info in household.sim_info_gen():
		relationships = sim_info.relationship_tracker
		for relationship in relationships:
			target_id = relationship.target_sim_id
			output('Got sim ID: {}'.format(target_id))
			target_sim = services.sim_info_manager().get(target_id)
			tracks = sim_info.relationship_tracker.relationship_tracks_gen(target_id)
			for track in tracks:
				if track.stat_type == track.ROMANCE_TRACK:
					decay = track.get_decay_rate_modifier() * 100
					output("Decay rate for {} {}'s romance bar with {} {} is {} percent of normal rate".format(sim_info.first_name, sim_info.last_name, target_sim.first_name, target_sim.last_name, decay))
				elif track.stat_type == track.FRIENDSHIP_TRACK:
					decay = track.get_decay_rate_modifier() * 100
					output("Decay rate for {} {}'s friendship bar with {} {} is {} percent of normal rate".format(sim_info.first_name, sim_info.last_name, target_sim.first_name, target_sim.last_name, decay))

