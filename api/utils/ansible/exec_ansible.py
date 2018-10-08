from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
import json

exec_result = {}
 
class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in
 
    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result
        This method could store the result in an instance attribute for retrieval later
        """
        global exec_result
        host = result._host
        self.data = json.dumps({host.name: result._result}, indent=4)
        exec_result = dict(exec_result,**json.loads(self.data))
 
 
def exec_ansible(module,args,host):               
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
    # initialize needed objects
    loader = DataLoader()
    options = Options(connection='ssh', module_path='/usr/local/lib/python3.6/site-packages/ansible-2.4.1.0-py3.6.egg/ansible/modules/', forks=100, become=None, become_method=None, become_user=None, check=False,diff=False)
    passwords = dict(vault_pass='secret')
 
    # Instantiate our ResultCallback for handling results as they come in
    results_callback = ResultCallback()
 
    # create inventory and pass to var manager
    inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
 
    # create play with tasks
    play_source =  dict(
            name = "Ansible Play",
            hosts = host,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=module, args=args), register='shell_out'),
             ]
        )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
 
    # actually run it
    tqm = None
    global exec_result
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  options=options,
                  passwords=passwords,
                  stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
              )
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()
        return exec_result
