from ConfigSpace import CategoricalHyperparameter, ConfigurationSpace
import time
from smac import HyperparameterOptimizationFacade, Scenario, initial_design
from smac.model.gaussian_process import kernels, GaussianProcess
import numpy as np

class HintSpace:
    def __init__(self, dbms, sql_path, seed):
        self.seed = seed
        self.search_space = ConfigurationSpace()
        self.dbms = dbms
        self.sql_path = sql_path
        self.options = ['on', "off"]
        self.knobs = ["enable_hashjoin", "enable_mergejoin", "enable_nestloop", "enable_seqscan", "enable_indexscan", "enable_indexonlyscan"]
        self.define_search_space()

    def define_search_space(self):
        for knob in self.knobs:
            normal_para = CategoricalHyperparameter(
                knob,
                [str(value) for value in self.options],
                default_value = "on",
            )
            self.search_space.add_hyperparameter(normal_para)

    def set_and_replay(self, config, seed=0):
        # self.dbms.reset_config()
        with open(self.sql_path, 'r') as file:
            query = file.read()
        for knob in self.knobs:
            value = config[knob]
            self.dbms.set_knob_session(knob, value)
        # self.dbms.reconfigure()
        start = time.time()
        self.dbms.get_sql_result(query)
        stop = time.time()
        return float(stop - start)
    
    def optimize(self, name, trials_number, initial_config_number):
        scenario = Scenario(
            configspace=self.search_space,
            name=name,
            seed=self.seed,
            deterministic=True,
            n_trials=trials_number,
            use_default_config=True,

        )
        init_design = initial_design.LatinHypercubeInitialDesign(
            scenario,
            n_configs=initial_config_number,
            max_ratio=0.8,  
        )
        kernel1 = kernels.HammingKernel(operate_on=np.array([0,1,2]))
        kernel2 = kernels.HammingKernel(operate_on=np.array([3,4,5]))
        kernel = kernels.ProductKernel(kernel1, kernel2)
        gp_model = GaussianProcess(configspace=self.search_space, kernel=kernel)
        smac = HyperparameterOptimizationFacade(
            scenario=scenario,
            initial_design=init_design,
            model = gp_model,
            target_function=self.set_and_replay,
            overwrite=False,
        )
        
        smac.optimize()
