import os
import sys
import json
import argparse
from argparse import Namespace
from BIRD_Interact.bird_interact_conv.code import (
    infer_api_system,
    call_api,
    collect_response,
    infer_api_user_1,
    infer_api_user_2,
    wrap_up_sql,
)

# --- SCRIPT CONFIGURATION ---
def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Python pipeline for BIRD-Interact.")
    parser.add_argument("--patience", type=int, default=3, help="Patience parameter.")
    parser.add_argument("--us_model_name", type=str, default="gpt-4.1-mini", help="User simulator model name.")
    parser.add_argument("--system_model_name", type=str, default="gpt-4.1-mini", help="System model name.")
    parser.add_argument("--project_root", type=str, default="BIRD-Interact", help="Root directory of the project.")
    return parser.parse_args()

def setup_environment(project_root):
    """Add necessary paths to sys.path and import project modules."""
    code_path = os.path.join(project_root, "bird_interact_conv", "code")
    eval_path = os.path.join(project_root, "evaluation", "src")
    
    if code_path not in sys.path:
        sys.path.append(code_path)
    if eval_path not in sys.path:
        sys.path.append(eval_path)


def is_file_non_empty(filepath):
    """Check if a file exists and is not empty."""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def get_max_turn(jsonl_file):
    """Extracts the maximum 'max_turn' value from a JSONL file."""
    max_val = 0
    if not is_file_non_empty(jsonl_file):
        print(f"Warning: {jsonl_file} not found or is empty. Cannot determine max_turn.")
        return 1 # Return a default to avoid loop errors, might need adjustment
        
    with open(jsonl_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                turn = data.get("max_turn")
                if isinstance(turn, int) and turn > max_val:
                    max_val = turn
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
    return max_val

# --- HELPER FUNCTIONS FOR PIPELINE STEPS ---

def run_system_step(paths, args, turn_num, phase=None):
    """Runs the System step: Prompt Gen -> API Call -> Response Collection."""
    print(f"\n--- Running System Step | Turn: {turn_num} | Phase: {phase or 'ambiguity'} ---")
    
    # 1. Prompt Generation
    prompt_gen_args = Namespace(
        prompt_path=paths['data_path'],
        result_path=paths['result_path_prompt'],
        user_resp_path=paths['user_resp_path'],
        DB_schema_path=paths['db_schema_path'],
        external_kg_path=paths['external_kg_path'],
        patience=args.patience,
        turn_num=turn_num,
        phase=phase
    )
    infer_api_system.main(prompt_gen_args)

    if not is_file_non_empty(paths['result_path_prompt']):
        print("Empty prompt file generated. Skipping API call and collection.")
        return
        
    # 2. Infer API
    api_args = Namespace(
        model_name=args.system_model_name,
        prompt_path=paths['result_path_prompt'],
        output_path=paths['result_path_response']
    )
    call_api.main(api_args)
    
    # 3. Response Collection
    collect_args = Namespace(
        source_path=paths['collect_source_path'],
        response_path=paths['result_path_response'],
        result_path=paths['result_path_selected_llm']
    )
    collect_response.main(collect_args)

def run_user_step1(paths, args, turn_num):
    """Runs User Simulator Step 1 (Parser)."""
    print(f"--- Running User Simulator Step 1 (Parser) | Turn: {turn_num} ---")
    
    # 1. Prompt Generation
    prompt_gen_args = Namespace(
        prompt_path=paths['user_1_path'],
        result_path=paths['result_path_prompt'],
        sys_resp_path=paths['sys_resp_path'],
        DB_schema_path=paths['db_schema_path'],
        turn_num=turn_num
    )
    infer_api_user_1.main(prompt_gen_args)

    if not is_file_non_empty(paths['result_path_prompt']):
        print("Empty prompt file generated. Skipping API call and collection.")
        return
        
    # 2. Infer API
    api_args = Namespace(
        model_name=args.us_model_name,
        prompt_path=paths['result_path_prompt'],
        output_path=paths['user_1_response_path']
    )
    call_api.main(api_args)
    
    # 3. Response Collection
    collect_args = Namespace(
        source_path=paths['collect_source_path'],
        response_path=paths['user_1_response_path'],
        result_path=paths['user_1_result_path']
    )
    collect_response.main(collect_args)

def run_user_step2(paths, args, turn_num):
    """Runs User Simulator Step 2 (Generator)."""
    print(f"--- Running User Simulator Step 2 (Generator) | Turn: {turn_num} ---")
    
    # 1. Prompt Generation
    prompt_gen_args = Namespace(
        prompt_path=paths['user_2_path'],
        result_path=paths['result_path_prompt'],
        sys_resp_path=paths['sys_resp_path'],
        user_1_resp_path=paths['user_1_resp_path'],
        DB_schema_path=paths['db_schema_path'],
        turn_num=turn_num
    )
    infer_api_user_2.main(prompt_gen_args)

    if not is_file_non_empty(paths['result_path_prompt']):
        print("Empty prompt file generated. Skipping API call and collection.")
        return
        
    # 2. Infer API
    api_args = Namespace(
        model_name=args.us_model_name,
        prompt_path=paths['result_path_prompt'],
        output_path=paths['user_2_response_path']
    )
    call_api.main(api_args)
    
    # 3. Response Collection
    collect_args = Namespace(
        source_path=paths['collect_source_path'],
        response_path=paths['user_2_response_path'],
        result_path=paths['user_2_result_path']
    )
    collect_response.main(collect_args)

def run_sql_extraction(paths, follow_up_path=None):
    """Extracts SQL from the final interaction file."""
    print("\n--- Running SQL Extraction ---")
    args = Namespace(
        data_path=paths['data_path'],
        result_path=paths['result_path_sql'],
        follow_up_path=follow_up_path
    )
    wrap_up_sql.main(args)

def run_evaluation(jsonl_file):
    """Runs the evaluation script on the generated SQL file."""
    print(f"\n--- Running Evaluation on {os.path.basename(jsonl_file)} ---")
    if not is_file_non_empty(jsonl_file):
        print("SQL result file is empty or does not exist. Skipping evaluation.")
        return
    args = Namespace(jsonl=jsonl_file)
    eval_bird_interact_batch.main(args)


# --- MAIN EXECUTION ---
def main():
    args = parse_arguments()
    setup_environment(args.project_root)

    # =====================================
    #  Basic Configurations & Path Setup
    # =====================================
    p, pr = args.patience, args.project_root
    sm_name = args.system_model_name
    
    # Base Directories
    result_dir = os.path.join(pr, "bird_interact_conv", "results", f"patience_{p}", sm_name)
    data_dir = os.path.join(pr, "bird_interact_conv", "data", "bird-interact-lite")
    os.makedirs(result_dir, exist_ok=True)
    
    # Common File Paths
    paths = {
        'db_schema_path': os.path.join(data_dir, "[[DB_name]]", "[[DB_name]]_schema.txt"),
        'external_kg_path': os.path.join(data_dir, "[[DB_name]]", "[[DB_name]]_kb.jsonl"),
        'initial_data': os.path.join(data_dir, "bird_interact_data.jsonl"),
        # System paths
        'sys_interaction_file': os.path.join(result_dir, "system_interaction.jsonl"),
        'result_path_prompt': os.path.join(result_dir, "system_interaction_prompt.jsonl"),
        'result_path_response': os.path.join(result_dir, "system_interaction_response.jsonl"),
        # User 1 paths
        'user_1_interaction_file': os.path.join(result_dir, "user_1_interaction.jsonl"),
        'user_1_response_path': os.path.join(result_dir, "user_1_interaction_response.jsonl"),
        # User 2 paths
        'user_2_interaction_file': os.path.join(result_dir, "user_2_interaction.jsonl"),
        'user_2_response_path': os.path.join(result_dir, "user_2_interaction_response.jsonl"),
    }
    
    # ========================================================================================
    #  Phase 1: Ambiguity Resolution
    # ========================================================================================
    print("========================= Phase 1: Ambiguity Resolution =========================")
    
    # --- Turn 1 ---
    turn_num = 1
    
    # System Step
    sys_paths = {
        'data_path': paths['sys_interaction_file'] if os.path.exists(paths['sys_interaction_file']) else paths['initial_data'],
        'user_resp_path': paths['initial_data'],
        'collect_source_path': paths['initial_data'],
        'result_path_selected_llm': paths['sys_interaction_file'],
        **paths
    }
    run_system_step(sys_paths, args, turn_num)
    
    # User Simulator Step 1
    user1_paths = {
        'user_1_path': paths['user_1_interaction_file'] if os.path.exists(paths['user_1_interaction_file']) else paths['initial_data'],
        'sys_resp_path': paths['sys_interaction_file'],
        'result_path_prompt': os.path.join(result_dir, "user_1_interaction_prompt.jsonl"),
        'user_1_response_path': paths['user_1_response_path'],
        'collect_source_path': paths['initial_data'],
        'user_1_result_path': paths['user_1_interaction_file'],
        'db_schema_path': paths['db_schema_path']
    }
    run_user_step1(user1_paths, args, turn_num)
    
    # User Simulator Step 2
    user2_paths = {
        'user_2_path': paths['user_2_interaction_file'] if os.path.exists(paths['user_2_interaction_file']) else paths['initial_data'],
        'sys_resp_path': paths['sys_interaction_file'],
        'user_1_resp_path': paths['user_1_interaction_file'],
        'result_path_prompt': os.path.join(result_dir, "user_2_interaction_prompt.jsonl"),
        'user_2_response_path': paths['user_2_response_path'],
        'collect_source_path': paths['initial_data'],
        'user_2_result_path': paths['user_2_interaction_file'],
        'db_schema_path': paths['db_schema_path']
    }
    run_user_step2(user2_paths, args, turn_num)
    
    # --- Remaining Turns ---
    max_turn = get_max_turn(paths['sys_interaction_file'])
    for i in range(2, max_turn):
        turn_num = i
        # System
        sys_paths_loop = sys_paths.copy()
        sys_paths_loop.update({
            'data_path': paths['sys_interaction_file'],
            'user_resp_path': paths['user_2_interaction_file'],
            'collect_source_path': paths['sys_interaction_file'],
        })
        run_system_step(sys_paths_loop, args, turn_num)
        
        # User 1
        user1_paths_loop = user1_paths.copy()
        user1_paths_loop.update({
            'user_1_path': paths['user_1_interaction_file'],
            'collect_source_path': paths['user_1_interaction_file'],
        })
        run_user_step1(user1_paths_loop, args, turn_num)
        
        # User 2
        user2_paths_loop = user2_paths.copy()
        user2_paths_loop.update({
            'user_2_path': paths['user_2_interaction_file'],
            'collect_source_path': paths['user_2_interaction_file'],
        })
        run_user_step2(user2_paths_loop, args, turn_num)

    # --- Final Turn: Gen SQL ---
    turn_num = max_turn
    final_sys_paths = {
        'data_path': paths['sys_interaction_file'],
        'user_resp_path': paths['user_2_interaction_file'],
        'collect_source_path': paths['sys_interaction_file'],
        'result_path_selected_llm': paths['sys_interaction_file'],
        **paths
    }
    run_system_step(final_sys_paths, args, turn_num)
    
    # --- SQL Extract & Eval ---
    sql_paths = {'data_path': paths['sys_interaction_file'], 'result_path_sql': os.path.join(result_dir, "sql_results.jsonl")}
    run_sql_extraction(sql_paths)
    run_evaluation(sql_paths['result_path_sql'])

    # ========================================================================================
    #  Phase 1 Debugging: One More Chance for Debugging
    # ========================================================================================
    print("\n=============== Phase 1 Debugging: One More Chance for Debugging ===============")
    debug_paths = {
        'data_path': paths['sys_interaction_file'],
        'user_resp_path': os.path.join(result_dir, "sql_results_output_with_status.jsonl"),
        'collect_source_path': paths['sys_interaction_file'],
        'result_path_selected_llm': paths['sys_interaction_file'],
        **paths
    }
    run_system_step(debug_paths, args, turn_num, phase='debug')
    
    debug_sql_paths = {'data_path': paths['sys_interaction_file'], 'result_path_sql': os.path.join(result_dir, "sql_results_debug.jsonl")}
    run_sql_extraction(debug_sql_paths)
    run_evaluation(debug_sql_paths['result_path_sql'])
    
    # ========================================================================================
    #  Phase 2: Follow Up Question
    # ========================================================================================
    print("\n========================= Phase 2: Follow Up Question =========================")
    follow_up_paths = {
        'data_path': paths['sys_interaction_file'],
        'user_resp_path': os.path.join(result_dir, "sql_results_debug_output_with_status.jsonl"),
        'collect_source_path': paths['sys_interaction_file'],
        'result_path_selected_llm': paths['sys_interaction_file'],
        **paths
    }
    run_system_step(follow_up_paths, args, turn_num, phase='follow')
    
    fu_sql_paths = {'data_path': paths['sys_interaction_file'], 'result_path_sql': os.path.join(result_dir, "sql_results_fu.jsonl")}
    run_sql_extraction(fu_sql_paths, follow_up_path=paths['result_path_prompt'])
    run_evaluation(fu_sql_paths['result_path_sql'])
    
    # ========================================================================================
    #  Phase 2 Debugging: One more chance for Follow Up question Debugging
    # ========================================================================================
    print("\n========== Phase 2 Debugging: One More Chance for Follow Up Debugging ==========")
    fu_debug_paths = {
        'data_path': paths['sys_interaction_file'],
        'user_resp_path': os.path.join(result_dir, "sql_results_fu_output_with_status.jsonl"),
        'collect_source_path': paths['sys_interaction_file'],
        'result_path_selected_llm': paths['sys_interaction_file'],
        **paths
    }
    run_system_step(fu_debug_paths, args, turn_num, phase='debug')
    
    fu_debug_sql_paths = {'data_path': paths['sys_interaction_file'], 'result_path_sql': os.path.join(result_dir, "sql_results_fu_debug.jsonl")}
    run_sql_extraction(fu_debug_sql_paths, follow_up_path=paths['result_path_prompt'])
    run_evaluation(fu_debug_sql_paths['result_path_sql'])

if __name__ == '__main__':
    main()