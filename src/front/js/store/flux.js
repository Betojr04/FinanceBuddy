const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      message: null,
      demo: [
        {
          title: "FIRST",
          background: "white",
          initial: "white",
        },
        {
          title: "SECOND",
          background: "white",
          initial: "white",
        },
      ],
    },
    actions: {
      // Use getActions to call a function within a fuction
      registerUser: async (email, password) => {
        try {
          const response = await fetch(
            process.env.BACKEND_URL + "api/register",
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ email, password }),
            }
          );

          if (response.ok) {
            const data = await response.json();
            console.log("Registration successful", data);
            // You can store the access token here if needed
            // setStore({ token: data.access_token });
          } else {
            console.error("Registration failed");
          }
        } catch (error) {
          console.error("Error during registration", error);
        }
      },
      loginUser: async (email, password) => {
        try {
          const response = await fetch(process.env.BACKEND_URL + "api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
          });

          if (response.ok) {
            const data = await response.json();
            console.log("Login successful", data);
            setStore({ token: data.access_token });
          } else {
            const errorData = await response.json();
            console.error("Login failed", errorData.msg);
            setStore({ loginError: errorData.msg });
          }
        } catch (error) {
          console.error("Error during login", error);
          setStore({ loginError: "An error occurred during login." });
        }
      },

      getMessage: async () => {
        try {
          // fetching data from the backend
          const resp = await fetch(process.env.BACKEND_URL + "api/hello");
          const data = await resp.json();
          setStore({ message: data.message });
          // don't forget to return something, that is how the async resolves
          return data;
        } catch (error) {
          console.log("Error loading message from backend", error);
        }
      },
      changeColor: (index, color) => {
        //get the store
        const store = getStore();

        //we have to loop the entire demo array to look for the respective index
        //and change its color
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });

        //reset the global store
        setStore({ demo: demo });
      },
    },
  };
};

export default getState;
