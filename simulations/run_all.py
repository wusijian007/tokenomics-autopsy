"""Run every death-spiral simulation and (re)generate all charts."""
import importlib

MODULES = [
    "sim1_algo_stable_absorbing_barrier",
    "sim2_olympus_33_unraveling",
    "sim3_p2e_faucet_sink",
    "sim4_bank_run_diamond_dybvig",
    "sim5_lvr_rented_liquidity",
    "sim6_governance_capture",
    "sim7_pid_damping",
    "sim8_spender_class",
]

if __name__ == "__main__":
    for name in MODULES:
        print("=" * 70)
        importlib.import_module(name).main()
    print("=" * 70)
    print("All charts written to ./charts/")
