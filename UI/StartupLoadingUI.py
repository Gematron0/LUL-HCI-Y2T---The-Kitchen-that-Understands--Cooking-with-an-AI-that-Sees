# this file contains AI

import base64
import random
import time
import streamlit as st
import streamlit.components.v1 as components


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def start(app_ui):
    placeholder = app_ui.empty()

    # Encode the local PNG image once so all layers share the same data string
    img_base64 = get_base64_image("UI/StartupBackground.png")

    with placeholder.container(height=600, border=False):
        # Keep Streamlit's content above all background layers (z-index: 1)
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] > .main {
                position: relative;
                z-index: 1;
                background: transparent;
            }
            div[data-testid="stProgress"] {
                margin-bottom: -24px;
            }
            .stProgress > div > div > div > div {
                background-color: red;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Inject multiple lazy/floaty image layers behind the text
        components.html(
            f"""
            <script>
            const parentDoc = window.parent.document;
            const appContainer = parentDoc.querySelector('[data-testid="stAppViewContainer"]') || parentDoc.body;

            // Check if the container for our floating layers already exists
            let layerGroup = parentDoc.getElementById("custom-cursor-layer-group");
            if (!layerGroup) {{
                layerGroup = parentDoc.createElement("div");
                layerGroup.id = "custom-cursor-layer-group";
                appContainer.appendChild(layerGroup);

                const imgSrc = "data:image/png;base64,{img_base64}";

                // Customize size, floatiness (ease), opacity, and slight starting offset for each layer
                const layerConfigs = [
                    {{ width: "900px", ease: 0.008, opacity: "0.10", offsetX: -40, offsetY: -20 }},
                    {{ width: "550px", ease: 0.020, opacity: "0.15", offsetX: 50,  offsetY: 30  }},
                    {{ width: "300px", ease: 0.045, opacity: "0.20", offsetX: -20, offsetY: 40  }}
                ];

                let mouseX = window.parent.innerWidth / 2;
                let mouseY = window.parent.innerHeight / 2;

                // Create DOM elements and state tracking for each layer
                const layers = layerConfigs.map((cfg) => {{
                    const img = parentDoc.createElement("img");
                    img.src = imgSrc;

                    Object.assign(img.style, {{
                        position: "fixed",
                        top: "0px",
                        left: "0px",
                        width: cfg.width,
                        height: "auto",
                        opacity: cfg.opacity,
                        pointerEvents: "none",
                        zIndex: "0",
                        transform: "translate(-50%, -50%)"
                    }});

                    layerGroup.appendChild(img);

                    return {{
                        el: img,
                        ease: cfg.ease,
                        offsetX: cfg.offsetX,
                        offsetY: cfg.offsetY,
                        currentX: mouseX + cfg.offsetX,
                        currentY: mouseY + cfg.offsetY
                    }};
                }});

                parentDoc.addEventListener("mousemove", (e) => {{
                    mouseX = e.clientX;
                    mouseY = e.clientY;
                }});

                function animate() {{
                    // Stop the animation loop once stop() removes the layer group
                    if (!parentDoc.getElementById("custom-cursor-layer-group")) return;

                    layers.forEach((layer) => {{
                        const targetX = mouseX + layer.offsetX;
                        const targetY = mouseY + layer.offsetY;

                        layer.currentX += (targetX - layer.currentX) * layer.ease;
                        layer.currentY += (targetY - layer.currentY) * layer.ease;

                        layer.el.style.left = layer.currentX + "px";
                        layer.el.style.top = layer.currentY + "px";
                    }});

                    requestAnimationFrame(animate);
                }}

                requestAnimationFrame(animate);
            }}
            </script>
            """,
            height=0,
            width=0,
        )

        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

        st.markdown(
            "<h1 style='text-align: center;'>Welcome to the cookbook app</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h5 style='text-align: center;'>Thanks for waiting while we set some things up on our side</h5>",
            unsafe_allow_html=True,
        )

        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            master_progress_bar = st.progress(
                0, text="Please wait while we complete some final checks"
            )
            minor_progress_bar = st.progress(0, text="")

        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

        fun_facts = [
            "This project contains many different AIs",
            "This was only coded in 10 weeks",
            "idk something",
        ]

        fun_fact = random.choice(fun_facts)

        st.markdown(
            f'<p style="text-align: center; color: gray;">Fun fact: {fun_fact}</p>',
            unsafe_allow_html=True,
        )

    return placeholder, master_progress_bar, minor_progress_bar


def stop(placeholder):
    # Remove the wrapper div to clean up all floating layers at once
    components.html(
        """
        <script>
        const group = window.parent.document.getElementById("custom-cursor-layer-group");
        if (group) {
            group.remove();
        }
        </script>
        """,
        height=0,
        width=0,
    )
    placeholder.empty()
