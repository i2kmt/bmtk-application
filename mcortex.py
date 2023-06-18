from bmtk.builder.networks import NetworkBuilder

net = NetworkBuilder('mcortex')
net.add_nodes(
    cell_name='Scnn1a_473845048',
    potential='exc',
    model_type='biophysical',
    model_template='ctdb:Biophys1.hoc',
    model_processing='aibs_perisomatic',
    dynamics_params='472363762_fit.json',
    morphology='Scnn1a_473845048_m.swc'
)

net.build()
net.save_nodes(output_dir='sim_ch01/network')

for node in net.nodes():
    print(node)

from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(
    base_dir='sim_ch01',       # Where to save the scripts and config files
    config_file='config.json', # Where main config will be saved.
    network_dir='network',     # Location of directory containing network files
    tstop=2000.0, dt=0.1,      # Run a simulation for 2000 ms at 0.1 ms intervals
    report_vars=['v', 'cai'],  # Tells simulator we want to record membrane potential and calcium traces
    current_clamp={            # Creates a step current from 500.0 ms to 1500.0 ms
        'amp': 0.120,
        'delay': 500.0,
        'duration': 1000.0
    },
    include_examples=True,    # Copies components files for tutorial examples
    compile_mechanisms=True   # Will try to compile NEURON mechanisms
)

from bmtk.simulator import bionet

conf = bionet.Config.from_json('sim_ch01/config.json')
conf.build_env()
conf
net = bionet.BioNetwork.from_config(conf)
sim = bionet.BioSimulator.from_config(conf, network=net)
sim.run()

from bmtk.analyzer.spike_trains import to_dataframe

to_dataframe(config_file='sim_ch01/config.json')

from bmtk.analyzer.compartment import plot_traces

_ = plot_traces(config_file='sim_ch01/config.json', node_ids=[0], report_name='v_report')
_ = plot_traces(config_file='sim_ch01/config.json', node_ids=[0], report_name='cai_report')