import streamlit as st

# Display the image at the top
st.image('legend.png', caption='Legend of the various parameters', use_column_width=True)

st.title("Epistemic Leverage Simulator")

# Mode Selector
mode = st.radio("Select Mode", ("Score Function Exploration", "Network Dynamics Simulation"))

if mode == "Score Function Exploration":
    st.header("Mode 1: Score Function Exploration")

    # Create two columns for inputs and outputs
    col1, col2 = st.columns(2)

    with col1:
        # Inputs for local modifiables and game context
        st.subheader("Stake Inputs")
        # Stakes
        q_k = st.number_input("Stake in q (q_k)", min_value=0.0, value=10.0, step=1.0)
        p_k = st.number_input("Stake in p (p_k)", min_value=0.0, value=5.0, step=1.0)
        x_k = st.number_input("Restake amount into x (x_k)", min_value=0.0, max_value=q_k, value=5.0, step=1.0)
        x_d = st.number_input("Doubt against x (x_d)", min_value=0.0, max_value=x_k, value=3.0, step=1.0)

        # Game context (scores of other nodes)
        st.subheader("Game Context (Direct Score Inputs)")
        r_s = st.number_input("Score of r (r_s)", min_value=0.0, value=2.0, step=1.0)
        y_s = st.number_input("Score of y (y_s)", min_value=0.0, value=1.0, step=1.0)
        o_s = st.number_input("Score of o (o_s)", min_value=0.0, value=4.0, step=1.0)
        z_s = st.number_input("Score of z (z_s)", min_value=0.0, value=3.0, step=1.0)

        # Parameter Constants
        st.subheader("Parameter Constants")
        k_const = st.number_input("Restaking bonus scaling constant (k_const)", min_value=0.0, value=1.0, step=0.1)
        d_const = st.number_input("Doubt penalty scaling constant (d_const)", min_value=0.0, value=1.0, step=0.1)
        v_const = st.number_input("Influence parameter (v_const)", min_value=0.0, value=1.0, step=0.1)
        a_const = st.number_input("Attenuation factor (a_const)", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    with col2:
        # Calculations
        st.header("Calculations")
        # Restaking bonus for x (x_b)
        x_s = x_k + x_d
        x_b = k_const * x_k * (p_k / x_s) if x_s > 0 else 0
        st.write(f"**Restaking bonus for x (x_b):** {x_b:.2f}")

        # Penalties from doubts
        x_penalty = d_const * x_d
        st.write(f"**Penalties from doubts against x (x_penalty):** {x_penalty:.2f}")

        # Influence on q from p and attenuated influence from z and o
        influence_on_q = v_const * (p_k + a_const * z_s + a_const**2 * o_s)
        st.write(f"**Influence on q (from p, z, o):** {influence_on_q:.2f}")

        # Score of q (q_s)
        q_s = q_k + x_b - x_penalty - influence_on_q
        q_s = max(q_s, 0)
        st.write(f"**Score of q (q_s):** {q_s:.2f}")

elif mode == "Network Dynamics Simulation":
    st.header("Mode 2: Network Dynamics Simulation")

    # Create two columns for inputs and outputs
    col1, col2 = st.columns(2)

    with col1:
        # Inputs for stakes, restakes, and doubts
        st.subheader("Stake Inputs")
        # Initial stakes
        q_k_A = st.number_input("Alice's stake in q (q_k_A)", min_value=0.0, value=10.0, step=1.0)
        p_k_B = st.number_input("Bob's stake in p (p_k_B)", min_value=0.0, value=5.0, step=1.0)
        o_k_Others = st.number_input("Others' stake in o (o_k_Others)", min_value=0.0, value=4.0, step=1.0)
        r_k_Others = st.number_input("Others' stake in r (r_k_Others)", min_value=0.0, value=2.0, step=1.0)
        y_k_Others = st.number_input("Others' stake in y (y_k_Others)", min_value=0.0, value=1.0, step=1.0)

        # Restakes
        x_k_A = st.number_input("Alice's restake into x (x_k_A)", min_value=0.0, max_value=q_k_A, value=5.0, step=1.0)
        x_d = st.number_input("Doubt against x (x_d)", min_value=0.0, max_value=x_k_A, value=3.0, step=1.0)

        z_k_B = st.number_input("Bob's restake into z (z_k_B)", min_value=0.0, max_value=p_k_B, value=2.0, step=1.0)
        z_d = st.number_input("Doubt against z (z_d)", min_value=0.0, max_value=z_k_B, value=1.0, step=1.0)

        # Parameter Constants
        st.subheader("Parameter Constants")
        k_const = st.number_input("Restaking bonus scaling constant (k_const)", min_value=0.0, value=1.0, step=0.1)
        d_const = st.number_input("Doubt penalty scaling constant (d_const)", min_value=0.0, value=1.0, step=0.1)
        v_const = st.number_input("Influence parameter (v_const)", min_value=0.0, value=1.0, step=0.1)
        a_const = st.number_input("Attenuation factor (a_const)", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

        # Simulation Parameters
        st.subheader("Simulation Parameters")
        max_iterations = st.number_input("Maximum iterations", min_value=1, value=10, step=1)
        convergence_threshold = st.number_input("Convergence threshold", min_value=0.0, value=0.01, step=0.01)

    with col2:
        st.header("Simulation Progress")
        # Initialize variables
        # Initial scores equal to stakes
        q_s = q_k_A
        p_s = p_k_B
        x_s = x_k_A + x_d
        z_s = z_k_B + z_d
        o_s = o_k_Others
        r_s = r_k_Others
        y_s = y_k_Others

        iteration = 0
        converged = False

        scores_history = []

        while iteration < max_iterations and not converged:
            iteration += 1

            # Previous scores
            q_s_prev = q_s
            p_s_prev = p_s
            x_s_prev = x_s
            z_s_prev = z_s

            # Restaking bonuses
            x_b = k_const * x_k_A * (p_s / x_s) if x_s > 0 else 0
            z_b = k_const * z_k_B * (q_s / z_s) if z_s > 0 else 0

            # Penalties from doubts
            x_penalty = d_const * x_d
            z_penalty = d_const * z_d

            # Influence calculations with attenuation
            influence_on_q = min(v_const * (p_s + a_const * z_s + a_const**2 * o_s), q_k_A + x_b)
            influence_on_p = min(v_const * (q_s + a_const * x_s + a_const**2 * r_s), p_k_B + z_b)
            influence_on_x = v_const * a_const * y_s  # Influence on x from y
            influence_on_z = v_const * a_const * o_s  # Influence on z from o

            # Update scores
            q_s = q_k_A + x_b - x_penalty - influence_on_q
            q_s = max(q_s, 0)
            p_s = p_k_B + z_b - z_penalty - influence_on_p
            p_s = max(p_s, 0)

            # Update restaking targets
            x_s = x_k_A + x_b - x_penalty - influence_on_x
            x_s = max(x_s, 0)
            z_s = z_k_B + z_b - z_penalty - influence_on_z
            z_s = max(z_s, 0)

            # For simplicity, assume o_s, r_s, y_s remain constant (others' stakes)

            # Record scores
            scores_history.append({
                'Iteration': iteration,
                'q_s': q_s,
                'p_s': p_s,
                'x_s': x_s,
                'z_s': z_s,
                'o_s': o_s,
                'r_s': r_s,
                'y_s': y_s
            })

            # Check for convergence
            delta_q = abs(q_s - q_s_prev)
            delta_p = abs(p_s - p_s_prev)
            delta_x = abs(x_s - x_s_prev)
            delta_z = abs(z_s - z_s_prev)

            if all(delta < convergence_threshold for delta in [delta_q, delta_p, delta_x, delta_z]):
                converged = True

        st.write(f"Simulation completed in {iteration} iterations.")

        # Display scores history
        st.subheader("Scores Over Iterations")
        st.write("Scores are rounded to two decimal places for readability.")
        st.table([{k: round(v, 2) if isinstance(v, float) else v for k, v in row.items()} for row in scores_history])

        # Final scores
        st.subheader("Final Scores")
        st.write(f"**Final Score of q (q_s):** {q_s:.2f}")
        st.write(f"**Final Score of p (p_s):** {p_s:.2f}")
        st.write(f"**Final Score of x (x_s):** {x_s:.2f}")
        st.write(f"**Final Score of z (z_s):** {z_s:.2f}")
        st.write(f"**Score of o (o_s):** {o_s:.2f}")
        st.write(f"**Score of r (r_s):** {r_s:.2f}")
        st.write(f"**Score of y (y_s):** {y_s:.2f}")

        # Token Prices (Normalized)
        st.subheader("Token Prices (Normalized)")
        total_score = q_s + p_s + x_s + z_s + o_s + r_s + y_s
        total_score = max(total_score, 1)  # Prevent division by zero

        token_price_q = q_s / total_score
        token_price_p = p_s / total_score
        token_price_x = x_s / total_score
        token_price_z = z_s / total_score
        token_price_o = o_s / total_score
        token_price_r = r_s / total_score
        token_price_y = y_s / total_score

        st.write(f"**Token price for q:** {token_price_q:.2f}")
        st.write(f"**Token price for p:** {token_price_p:.2f}")
        st.write(f"**Token price for x:** {token_price_x:.2f}")
        st.write(f"**Token price for z:** {token_price_z:.2f}")
        st.write(f"**Token price for o:** {token_price_o:.2f}")
        st.write(f"**Token price for r:** {token_price_r:.2f}")
        st.write(f"**Token price for y:** {token_price_y:.2f}")
