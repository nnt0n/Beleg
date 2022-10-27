import yaml
from mocasin.common.graph import DataflowChannel, DataflowGraph, DataflowProcess




class LF_To_Moc_graph(DataflowGraph):

    def __init__(self):
        super().__init__("Trace-Graph")
        self.generate_from_trace("/home/anton/Beleg/Beleg/src/Chameneos.yaml")


    def generate_from_trace(self, path):

        yaml_data = yaml.load(open(path), Loader=yaml.FullLoader)     
        dependencies = yaml_data['reaction_dependencies'] 

        channel_nr = 0   

        for i in range(0, len(dependencies), 2):

            sink_list = dependencies[i]["from"].split(".")[1:]
            src_list = dependencies[i+1]["to"].split(".")[1:]          

            src_name = src_list[0] + "." + src_list[1][-1]
            sink_name = sink_list[0] + "." + sink_list[1][-1]

            if src_name not in self.process_names():
                self.add_process(DataflowProcess(src_name))

            if sink_name not in self.process_names(): 
                self.add_process(DataflowProcess(sink_name))

            channel = DataflowChannel("c" + str(channel_nr), 1)
            self.add_channel(channel)

            src_proc = self.find_process(src_name)
            sink_proc = self.find_process(sink_name)

            src_proc.connect_to_outgoing_channel(channel)
            sink_proc.connect_to_incomming_channel(channel)

            channel_nr += 1        