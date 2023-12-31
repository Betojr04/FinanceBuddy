const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      message: null,
      token: null,
      accessToken: null,
      accounts: null,
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
      /**
       *
       * THIS IS FOR REGISTERING THE USER
       *
       */
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
      /**
       *
       * THIS IS FOR LOGGING IN THE USER
       *
       */
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
            localStorage.setItem("token", data.access_token);
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
      /**
       *
       * THIS IS FOR LOGGING OUT THE USER
       *
       */
      logoutUser: () => {
        // Remove the token from local storage or wherever it's stored
        localStorage.removeItem("token");
        // Update the global store
        setStore({ token: null });
      },
      setToken: (token) => {
        setStore({ token: token });
      },
      /**
       *
       * EXCHANGING THE PUBLIC TOKEN THAT WAS CREATED TO BE ABLE TO FETCH THE API FOR BANKING DETIALS
       *
       */
      exchangePublicToken: async (publicToken) => {
        try {
          const response = await fetch(
            `${process.env.BACKEND_URL}api/exchange_public_token`,
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ public_token: publicToken }),
            }
          );

          if (response.ok) {
            const data = await response.json();
            console.log("Access token exchange successful", data);
            setStore({ accessToken: data.access_token });
          } else {
            const errorData = await response.json();
            console.error("Access token exchange failed", errorData);
          }
        } catch (error) {
          console.error("Error during access token exchange", error);
        }
      },
      // Set Plaid's access token and fetch accounts
      setAccessToken: async (accessToken) => {
        setStore({ accessToken });
        await getActions().fetchAccounts();
      },

      // Clear Plaid's access token on logout or when needed
      clearAccessToken: () => {
        setStore({ accessToken: null });
      },
      /**
       *
       * THIS IS FOR FETCHING THE USERS ACCOUNT DATA
       *
       */
      fetchAccounts: async () => {
        try {
          const accessToken = getStore().accessToken;
          if (!accessToken) {
            throw new Error("Access token not available");
          }
          const response = await fetch(
            `${process.env.BACKEND_URL}api/accounts`,
            {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer + ${accessToken}`,
              },
            }
          );

          if (!response.ok) {
            throw new Error("Failed to fetch account data");
          }

          const data = await response.json();
          setStore({ accounts: data.accounts });
        } catch (error) {
          console.error("Error fetching account data:", error);
        }
      },

      /**
       *
       * THESE TWO BELOW ARE BOILERPLATE ACTIONS, NOT APART OF PERSONAL FINANCE APPLICATION
       *
       */
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
