# OpenAPI 3 + Connexion + AioHTTP tutorial

The purpose of this tutorial is to facilitate learning about the
[OpenAPI 3](https://github.com/OAI/OpenAPI-Specification/) spec +
[Connexion](https://connexion.readthedocs.io/en/latest/) +
[AioHTTP](https://aiohttp.readthedocs.io/en/latest/)
stack. And designing APIs according to the
[Google API Design Guide](https://cloud.google.com/apis/design/).
Also use of proper linting and Python formatting is encouraged through a pre-commit hook.
With some knowledge of how to use a shell (Mac/Linus/Unix - I prefer
[Bash](https://www.gnu.org/software/bash/)) + [Git](https://git-scm.com/) +
[Python 3](https://docs.python.org/3/), you should be able to have
this tutorial working for you pretty quickly. The interesting part of this tutorial is that there
are [Pytests](https://docs.pytest.org/en/latest/) for each step. This also works to demo
test driven development. Each part of the tutorial has a different pytest file and a
corresponding [Makefile](https://www.gnu.org/software/make/manual/html_node/Introduction.html)
entry to make running it simple. Answers for each step in the tutorial are included in different
Git branches named for the step.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Setup

This project requires [Docker](https://docs.docker.com/). Setup by following their instructions.

Once the project is cloned to your computer, dependencies must be installed.
Python dependencies should always be managed in a virtual environment, but setting up a virtual
environments is outside the scope of this tutorial.

Install the necessary [pip](https://pypi.org/project/pip/) packages listed in the
`requirements.txt` file. Installing and using `pip` is outside the scope of this tutorial.

### Running the AioHTTP server

If you can get the AioHTTP server running, then you know your environment is setup correctly for
the rest of the tutorials.

*Note* either you must run everything from the root of this project or add the project's directory
to your `PYTHONPATH`.

To begin, start up your docker containers via:

```bash
make docker
```

After the docker containers start up, you can run the app like:

```bash
make run
```

*Note* This will run your server in the foreground and monopolize the shell until you `CTRL+C`.

Then you can test the API by using `curl` in a new shell:

```bash
curl -v "http://127.0.0.1:9000/"
```

If you go to the URL in your browser, it will redirect you back to the Github project + README.

While the app is running, you can also view the local Swagger UI docs by opening your browser
to [localhost/ui](http://127.0.0.1:9000/ui/).

Once you are finished exploring, you can safely `CTRL+C` to shut down the web server.

### Running the tests

There are pytests which validate that you've correctly completed each step in this tutorial.
You can run the tests by executing:

```bash
make tests
```

The first time you run this all the tests will fail. This is expected. You'll be doing the
work in this tutorial to get the tests working.

### Before committing code

Finally, if you want to contribute code back to the project. Please setup the provided githooks.
You can do this with:

```bash
make githooks
```

## Passing the tests

Each of the tests will require a few steps to get it working. First, you should modify `index.yaml`
inside the `spec` folder. Each test will require adding new yaml under the `paths` directive.
In addition, for test #2 you should add a new item under the `components:schemas` for the Kudo
object which will be reused in tests #3 & #4.

### Test 1 - Hello World

To get test 1 passing, you'll need to do a few items:
* Update index.yaml. You can look at the included `/` path as an example.
    1. Add a `/hello-world` route to the index.yaml
    2. Add a GET method to the route with a summary and description.
    3. Add a combination of `x-openapi-router-controller` (*optional*) and `operationId` (*required*)
        attributes pointing to your function. Don't worry too much about the Google API Design
        Guide on this one.  It's just a 'Hello World'.
    4. Add a 200 response and description.
* Create your new handler file & function. You can look at `handlers/root.py` and
    [AIOHTTP docs](https://aiohttp.readthedocs.io/en/latest/web_quickstart.html#handler) to
    figure this part out. You *MUST* return a JSON object with a single key of `"Hello"` and it's
    corresponding value set to `"World"`. *Hint* don't forget the `Content-Type` header.
* After these changes, you can test your code. If you wish, you may use `make run` and hit your
    endpoint to see the results, or you can use the Makefile via `make test_1`.

### Test 2 - Kudos Collection - GET method

To get test 2 passing, you'll need to do the following:
* Update index.yaml.
    1. Add a `/kudos` route to the index.yaml. *Note* the Kudo schema is already defined for you
        in the `index.yaml` file under schemas. To make the tests pass use this schema.
    2. Add a GET method to the route with a summary and description.
    3. Add a combination of `x-openapi-router-controller` (*optional*) and `operationId` (*required*)
        attributes pointing to your function.
    4. Add a 200 response and description. It should return a Kudo schema.
* Create your new handler file & function. Remember to follow the
    [Google API Design Guide](https://cloud.google.com/apis/design/). *Note* You will run into
    an issue with Python's default `json.dumps` not being able to handle datetime objects. There
    are several clever workarounds, and it will be up to you to chose and implement one.
* It should read the existing kudo in the database using the `db_conn` setup in `main.py`. This
    is passed into the handler via the arg object which is an AioHTTP request class.
* A `kudo` resource should contain all the attributes listed in the `schema` of `index.yaml`.
* After these changes, you can test your code. If you wish, you may use `make run` and hit your
    endpoint to see the results, or you can use the Makefile via `make test_2`.

### Test 3 - Kudos Collection - POST method

To get test 3 passing, you'll need to do the following:
* Update index.yaml.
    1. Update the `/kudos` route in index.yaml and add a POST method. It should return the Kudo
        schema.
    2. Add a combination of `x-openapi-router-controller` (*optional*) and `operationId` (*required*)
        attributes pointing to your function.
    3. Add a 201 response and description. It should return a Kudo schema.
* Add your function to process the POST method. It should use the `db_conn` setup in `main.py`
    as in the previous step to save a new row to the database.
* The `kudo` resource returned should contain all the attributes listed in the `schema` of `index.yaml`.
* After these changes, you can test your code. If you wish, you may use `make run` and hit your
    endpoint to see the results, or you can use the Makefile via `make test_3`.

### Test 4 - Kudo Resource - GET method

To get test 4 passing, you'll need to do the following:
* Update index.yaml.
    1. Add the `/kudos/{id}` route in index.yaml and add a GET method. It should return the Kudo
        schema.
    2. Add a combination of `x-openapi-router-controller` (*optional*) and `operationId` (*required*)
        attributes pointing to your function.
    3. Add a 200 response and description. It should return a Kudo schema.
* Add your function and test your code.

### Test 5 - Kudo Resource - PUT method

To get test 5 passing, you'll need to do the following:
* Update index.yaml.
    1. Update the `/kudos/{id}` route in index.yaml and add a PUT method. It should take a kudo
        as input and return the Kudo schema.
    2. Add a combination of `x-openapi-router-controller` (*optional*) and `operationId` (*required*)
        attributes pointing to your function.
    3. Add a 200 response and description. It should return a Kudo schema.
* Add your function and test your code. *Note* make sure you update your `updated_dt` column with
    a new timestamp when the object is updated.

### Test 6 - Kudo Resource - DELETE method

To get test 6 passing, you'll need to do the following:
* Update index.yaml.
    1. Update the `/kudos/{id}` route in index.yaml and add a DELETE method. It should return a
        204 status and an empty body.
    2. Add a combination of `x-openapi-router-controller` (*optional*) and `operationId` (*required*)
        attributes pointing to your function.
    3. Add a 204 response and description.
* Add your function and test your code.
