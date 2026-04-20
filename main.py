
from pydriller import Repository
import statistics

repo_url = "https://github.com/apache/camel"
issue_ids = ["CAMEL-180", "CAMEL-321", "CAMEL-1818", "CAMEL-3214", "CAMEL-18065"]


def run_analysis():
    unique_commits = {}
    
    print("--- ANALYSIS STARTED ---")
    print(f"Connecting to: {repo_url}")
    print("Please wait, this can take a few minutes as the repo is very large...")

   
    for commit in Repository(repo_url).traverse_commits():
        
        # Issue IDs
        for issue in issue_ids:
            if issue in commit.msg:
                
                metrics = [commit.dmm_unit_size, 
                           commit.dmm_unit_complexity, 
                           commit.dmm_unit_interfacing]
                
                
                clean_metrics = [m for m in metrics if m is not None]
                avg_dmm = statistics.mean(clean_metrics) if clean_metrics else 0
                
                # Saving the results for this commit
                unique_commits[commit.hash] = {
                    "files": len(commit.modified_files),
                    "dmm": avg_dmm
                }
                break 

    # --- CALCULATING FINAL RESULTS ---
    total_found = len(unique_commits)
    
    if total_found > 0:
        avg_files = sum(c["files"] for c in unique_commits.values()) / total_found
        avg_dmm_global = sum(c["dmm"] for c in unique_commits.values()) / total_found
        
        print("\n--- FINAL RESULTS ---")
        print(f"Total Commits Found: {total_found}")
        print(f"Average Files Changed: {avg_files:.2f}")
        print(f"Average DMM Metric: {avg_dmm_global:.4f}")
        print("----------------------")
    else:
        print("\nNo commits were found matching those IDs.")


if __name__ == "__main__":
    run_analysis()

