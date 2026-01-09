"""
Example of timeout-based stopping with repeated runs.

This example supports repeated executions via command-line arguments:
- Instance name: which instance file to use
- Instance type: ``model`` or ``realworld``
- Per-run time limit: maximum runtime (seconds) for each run
- Number of repetitions: how many times to repeat the algorithm

Usage:
    python example.py grqc.txt realworld 3600 10

This strategy is useful in practice: it can prevent the algorithm from running
indefinitely and support batch experiments.
"""

import argparse
import os
import time

from pycnp import Model, read
from pycnp.MemeticSearch import MemeticSearchParams
from pycnp.stop import MaxRuntime
from pycnp.visualization import visualize_graph


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="PyCNP repeated-execution tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python example.py grqc.txt realworld 3600 10
  python example.py ErdosRenyi_n941.txt model 1800 5
        """,
    )

    parser.add_argument(
        "instance_name",
        help="Instance file name (without path)",
    )

    parser.add_argument(
        "instance_type",
        choices=["model", "realworld"],
        help="Instance type: 'model' or 'realworld'",
    )

    parser.add_argument(
        "runtime",
        type=int,
        help="Maximum runtime per run (seconds)",
    )

    parser.add_argument(
        "repetitions",
        type=int,
        help="Number of repetitions",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed (default: 42)",
    )

    parser.add_argument(
        "--budget",
        type=int,
        default=140,
        help="Algorithm budget parameter (default: 140)",
    )

    return parser.parse_args()


def save_result(run_id, result, runtime, output_path):
    """Append a single run's result to the same text file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    line = (
        f"Repeat = {run_id}, BestObjValue = {result.best_obj_value}, "
        f"BestTime = {runtime:.6f}\n"
    )
    with open(output_path, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"Result appended to: {output_path}")
    return output_path


def run_single_experiment(
    instance_name,
    instance_type,
    runtime,
    seed,
    budget,
    run_id,
    total_runs,
):
    """Run a single experiment."""
    print(f"\n{'=' * 80}")
    print(f"Starting run {run_id}/{total_runs}")
    print(f"Instance: {instance_name} ({instance_type})")
    print(f"Time limit per run: {runtime} seconds")
    print(f"Random seed: {seed}")
    print(f"{'=' * 80}")

    try:
        # Build file path
        instance_path = f"./Instances/CNP/{instance_type}/{instance_name}"
        print(f"Reading problem data from: {instance_path}")

        # Read problem data
        problem_data = read(instance_path)
        model = Model.from_data(problem_data)
        print("Problem data loaded.")

        # Configure algorithm parameters
        print("Configuring algorithm parameters...")
        # By default use problem reduction (RSC crossover),
        # consistent with the original implementation
        memetic_params = MemeticSearchParams(
            search="CHNS",
            is_problem_reduction=True,
            is_pop_variable=False,
            initial_pop_size=5,
        )
        print("Parameter configuration done.")

        # Configure stopping criteria
        print(f"Stopping criteria: run for {runtime} seconds")

        stopping_criterion = MaxRuntime(runtime)

        # Start solving
        print("Starting solver...")
        start_time = time.time()

        result = model.solve(
            problem_type="CNP",
            budget=budget,
            stopping_criterion=stopping_criterion,
            seed=seed,
            memetic_search_params=memetic_params,
            display=True,
        )
        visualize_graph(
            problem_data, result.best_solution, filename="interactive_graph.html"
        )

        end_time = time.time()
        actual_runtime = end_time - start_time
        print("Solving finished.")

        # Analyse result
        print(f"\n{'=' * 60}")
        print(f"Run {run_id} result")
        print(f"{'=' * 60}")

        print(f"Best solution: {result.best_solution}")
        print(f"Objective value: {result.best_obj_value}")
        print(f"Iterations: {result.num_iterations}")
        print(f"Actual runtime: {actual_runtime:.2f} seconds")

        # Determine stopping reason
        triggered = stopping_criterion.get_triggered_criterion()
        if triggered and triggered.get_name() == "MaxRuntime":
            print("⏰ Reached maximum runtime limit.")

        return result, actual_runtime

    except Exception as e:
        print(f"\nRun {run_id} failed with an error:")
        print(f"   Error type: {type(e).__name__}")
        print(f"   Error message: {e!s}")
        raise e


def main():
    """Main entry point - supports CLI arguments and repeated executions."""
    args = parse_arguments()

    print("=== PyCNP repeated-execution tool ===")
    print(f"Instance: {args.instance_name} ({args.instance_type})")
    print(f"Runtime per run: {args.runtime} seconds")
    print(f"Repetitions: {args.repetitions}")
    print(f"Random seed: {args.seed}")
    print(f"Budget parameter: {args.budget}")
    print()

    # Create results directory
    results_dir = f"results/{args.instance_type}"
    os.makedirs(results_dir, exist_ok=True)
    result_file_path = os.path.join(
        results_dir, f"{args.instance_name}_{args.instance_type}.txt"
    )
    with open(result_file_path, "w", encoding="utf-8") as f:
        f.write("")  # Clear file to record current experiment results

    # Store all run results
    all_results = []
    successful_runs = 0

    # Repeated execution loop
    for run_id in range(1, args.repetitions + 1):
        try:
            result, runtime = run_single_experiment(
                args.instance_name,
                args.instance_type,
                args.runtime,
                args.seed + run_id - 1,  # Use a different seed for each run
                args.budget,
                run_id,
                args.repetitions,
            )

            # Save result
            save_result(
                run_id,
                result,
                runtime,
                result_file_path,
            )

            all_results.append(
                {
                    "run_id": run_id,
                    "best_obj_value": result.best_obj_value,
                    "runtime": runtime,
                    "iterations": result.num_iterations,
                }
            )

            successful_runs += 1

        except Exception as e:
            print(f"\nRun {run_id} failed: {e!s}")
            continue

    # Print summary
    print(f"\n{'=' * 80}")
    print("Experiment summary")
    print(f"{'=' * 80}")
    print(f"Total runs: {args.repetitions}")
    print(f"Successful runs: {successful_runs}")
    print(f"Failed runs: {args.repetitions - successful_runs}")

    if successful_runs > 0:
        obj_values = [r["best_obj_value"] for r in all_results]
        runtimes = [r["runtime"] for r in all_results]

        print("\nResult statistics:")
        print(f"  Best objective: {min(obj_values)}")
        print(f"  Worst objective: {max(obj_values)}")
        print(f"  Average objective: {sum(obj_values) / len(obj_values):.2f}")
        print(f"  Average runtime: {sum(runtimes) / len(runtimes):.2f} seconds")

    print(f"\nAll results have been saved to: {results_dir}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
