# Reflection Loss - Engine

## Api Format

### Simulation Mode
- **Calculate Simulation**

  `POST: /calculate/simulation`
  - Request
    - JSON
      ```
      {
        "absorber_thickness": float,
        "frequency": {
          "start": float,
          "end": float,
          "num_data": int
        },
        "relative_permeability": {
          "real": float,
          "imag": float
        },
        "relative_permitivity": {
          "real": float,
          "imag": float
        },
        "option": {
          "show": {
            "impedance": boolean,
            "absorption": boolean
          },
          "savgol_filter": {
            "window_length": int,
            "polyorder": int
        }
        }
      }
      ```
      
  - Response
    ```
    {
      "frequency": {
        "label": Array<string>,
        "value": Array<float>
      },
      "impedance": {
        "real": Array<float>,
        "real_filter": Array<float>,
        "imag": Array<float>,
        "imag_filter": Array<float>
      },
      "reflection_loss": {
        "original": Array<float>,
        "filter": Array<float>
      }
    }
    ```

### Eksperiment Mode
- **Import Experiment Dataset**

  `POST: /api/data`
  - Request
    - FormData
      - data: csv file

  - Response
    ```
    {
      "message": string
      "key": string
    }
    ```

- **Get Experiment Dataset**

  `GET: /api/data`
  - Request
    - Header:
      - key: string
      
  - Response
    ```
    {
      "message": string
      "data": {
        "frequency": {
          "0": float
          ...
        },
        "s11r": {
          "0": float
          ...
        },
        "s11i": {
          "0": float
          ...
        },
        "s21r": {
          "0": float
          ...
        },
        "s21i": {
          "0": float
          ...
        },
        "s12r": {
          "0": float
          ...
        },
        "s12i": {
          "0": float
          ...
        },
        "s22r": {
          "0": float
          ...
        },
        "s22i": {
          "0": float
          ...
        }
      }
    }
    ```

- **Calculate Experiment**

  `POST: /calculate/simulation`

  - Request
    - Headers
      - key: string

    - JSON
      ```
      {
        thickness: float,
        option: {
        savgol_filter: {
            window_length: int,
            polyorder: 2
        }
    }
      }
      ```
  - Response
    ```
    {
      "frequency": {
        "label": Array<string>,
        "value": Array<float>,
      },
      "reflectance": {
        "real": Array<float>,
        "real_filter": Array<float>,
        "imag": Array<float>,
        "imag_filter": Array<float>,
      },
      "transmitance": {
        "real": Array<float>,
        "real_filter": Array<float>,
        "imag": Array<float>,
        "imag_filter": Array<float>,
      },
      "relative_permeability": {
        "real": Array<float>,
        "real_filter": Array<float>,
        "imag": Array<float>,
        "imag_filter": Array<float>,
      },
      "relative_permitivity": {
        "real": Array<float>,
        "real_filter": Array<float>,
        "imag": Array<float>,
        "imag_filter": Array<float>,
      },
      "impedance": {
        "real": Array<float>,
        "real_filter": Array<float>,
        "imag": Array<float>,
        "imag_filter": Array<float>,
      },
      "reflection_loss": {
        "original": Array<float>,
        "filter": Array<float>
      }
    }
    ```