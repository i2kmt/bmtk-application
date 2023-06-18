from bmtk.builder.networks import NetworkBuilder

cortex = NetworkBuilder('mcortex')
cortex.add_nodes(
    cell_name='Scnn1a_473845048',
    potental='exc',
    model_type='biophysical',
    model_template='ctdb:Biophys1.hoc',
    model_processing='aibs_perisomatic',
    dynamics_params='472363762_fit.json',
    morphology='Scnn1a_473845048_m.swc'
)

cortex.build()
cortex.save_nodes(output_dir='sim_ch02/network')

thalamus = NetworkBuilder('mthalamus')
thalamus.add_nodes(
    N=10,
    pop_name='tON',
    potential='exc',
    model_type='virtual'
)

thalamus.add_edges(
    source={'pop_name': 'tON'}, target=cortex.nodes(),
    connection_rule=5,
    syn_weight=0.001,
    delay=2.0,
    weight_function=None,
    target_sections=['basal', 'apical'],
    distance_range=[0.0, 150.0],
    dynamics_params='AMPA_ExcToExc.json',
    model_template='exp2syn'
)

thalamus.build()
thalamus.save_nodes(output_dir='sim_ch02/network')
thalamus.save_edges(output_dir='sim_ch02/network')

from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator

psg = PoissonSpikeGenerator(population='mthalamus')
psg.add(
    node_ids=range(10),  # Have 10 nodes to match mthalamus
    firing_rate=10.0,    # 10 Hz, we can also pass in a nonhomoegenous function/array
    times=(0.0, 3.0)    # Firing starts at 0 s up to 3 s
)
psg.to_sonata('sim_ch02/inputs/mthalamus_spikes.h5')

print('Number of spikes: {}'.format(psg.n_spikes()))
print('Units: {}'.format(psg.units()))

psg.to_dataframe().head()

from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(
    base_dir='sim_ch02',
    config_file='config.json',
    network_dir='sim_ch02/network',
    tstop=3000.0, dt=0.1,
    report_vars=['v', 'cai'],    # Record membrane potential and calcium (default soma)
    spikes_inputs=[('mthalamus', # Name of population which spikes will be generated for
                    'sim_ch02/inputs/mthalamus_spikes.h5')],
    include_examples=True,       # Copies components files
    compile_mechanisms=True      # Will try to compile NEURON mechanisms
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