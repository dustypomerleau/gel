.. _ref_guide_nextjs_app_router:

====================
Next.js (App Router)
====================

:edb-alt-title: Building a simple blog application with
   Gel and Next.js (App Router)

We're going to build a simple blog application with
`Next.js <https://nextjs.org/>`_ and Gel. Let's start by scaffolding our
app with Next.js's ``create-next-app`` tool.

You'll be prompted to provide a name (we'll use ``nextjs-blog``) for your
app and choose project options. For this tutorial, we'll go with the
recommended settings including TypeScript, App Router, and
**opt-ing out** of the ``src/`` directory.

.. code-block:: bash

  $ npx create-next-app@latest
    ✔ Would you like to use TypeScript? Yes
    ✔ Would you like to use ESLint? Yes
    ✔ Would you like to use Tailwind CSS? Yes
    ✔ Would you like to use src/ directory? No
    ✔ Would you like to use App Router? (recommended) Yes
    ✔ Would you like to customize the default import alias (@/*) Yes

The scaffolding tool will create a simple Next.js app and install its
dependencies. Once it's done, you can navigate to the app's directory and
start the development server.

.. code-block:: bash

  $ cd nextjs-blog
  $ npm dev # or yarn dev or pnpm dev or bun run dev

When the dev server starts, it will log out a local URL.
Visit that URL to see the default Next.js homepage. At this
point the app's file structure looks like this:

.. code-block::

  README.md
  tsconfig.json
  package.json
  next.config.js
  next-env.d.ts
  postcss.config.js
  tailwind.config.js
  app
  ├── page.tsx
  ├── layout.tsx
  ├── globals.css
  └── favicon.ico
  public
  ├── next.tsx
  └── vercel.svg

There's an async function ``Home`` defined in ``app/page.tsx`` that renders
the homepage. It's a
`Server Component <https://nextjs.org/docs/app/building-your-application/
rendering/server-components>`_
which lets you integrate server-side logic directly
into your React components. Server Components are executed on the server and
can fetch data from a database or an API. We'll use this feature to load blog
posts from a Gel database.

Updating the homepage
---------------------

Let's start by implementing a simple homepage for our blog application using
static data. Replace the contents of ``app/page.tsx`` with the following.

.. code-block:: tsx
  :caption: app/page.tsx

  import Link from 'next/link'

  type Post = {
    id: string
    title: string
    content: string
  }

  export default async function Home() {
    const posts: Post[] = [
      {
        id: 'post1',
        title: 'This one weird trick makes using databases fun',
        content: 'Use Gel',
      },
      {
        id: 'post2',
        title: 'How to build a blog with Gel and Next.js',
        content: "Let's start by scaffolding our app with `create-next-app`.",
      },
    ]

    return (
      <div className="container mx-auto p-4 bg-black text-white">
        <h1 className="text-3xl font-bold mb-4">Posts</h1>
        <ul>
          {posts.map((post) => (
            <li
              key={post.id}
              className="mb-4"
            >
              <Link
                href={`/post/${post.id}`}
                className="text-blue-500"
              >
                {post.title}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    )
  }


After saving, you can refresh the page to see the blog posts. Clicking on a
post title will take you to a page that doesn't exist yet. We'll create that
page later in the tutorial.

Initializing Gel
----------------

Now let's spin up a database for the app. You have two options to initialize
a Gel project: using ``$ npx gel`` without installing the CLI, or
installing the gel CLI directly. In this tutorial, we'll use the first
option. If you prefer to install the CLI, see the
:ref:`Gel CLI guide <ref_cli_overview>` for more information.

From the application's root directory, run the following command:

.. code-block:: bash

  $ npx gel project init
  No `gel.toml` found in `~/nextjs-blog` or above
  Do you want to initialize a new project? [Y/n]
  > Y
  Specify the name of Gel instance to use with this project [default:
  nextjs_blog]:
  > nextjs_blog
  Checking Gel versions...
  Specify the version of Gel to use with this project [default: x.x]:
  >
  ┌─────────────────────┬──────────────────────────────────────────────┐
  │ Project directory   │ ~/nextjs-blog                                │
  │ Project config      │ ~/nextjs-blog/gel.toml                       │
  │ Schema dir (empty)  │ ~/nextjs-blog/dbschema                       │
  │ Installation method │ portable package                             │
  │ Start configuration │ manual                                       │
  │ Version             │ x.x                                          │
  │ Instance name       │ nextjs_blog                                  │
  └─────────────────────┴──────────────────────────────────────────────┘
  Initializing Gel instance...
  Applying migrations...
  Everything is up to date. Revision initial.
  Project initialized.

This process has spun up a Gel instance called ``nextjs_blog`` and
associated it with your current directory. As long as you're inside that
directory, CLI commands and client libraries will be able to connect to the
linked instance automatically, without additional configuration.

To test this, run the |gelcmd| command to open a REPL to the linked instance.

.. code-block:: bash

  $ gel
  Gel x.x (repl x.x)
  Type \help for help, \quit to quit.
  gel> select 2 + 2;
  {4}
  >

From inside this REPL, we can execute EdgeQL queries against our database. But
there's not much we can do currently, since our database is schemaless. Let's
change that.

The project initialization process also created a new subdirectory in our
project called ``dbschema``. This is folder that contains everything
pertaining to Gel. Currently it looks like this:

.. code-block::

  dbschema
  ├── default.gel
  └── migrations

The :dotgel:`default` file will contain our schema. The ``migrations``
directory is currently empty, but will contain our migration files. Let's
update the contents of :dotgel:`default` with the following simple blog schema.

.. code-block:: sdl
  :caption: dbschema/default.gel

  module default {
    type BlogPost {
      required title: str;
      required content: str {
        default := ""
      }
    }
  }

.. note::

  Gel lets you split up your schema into different ``modules`` but it's
  common to keep your entire schema in the ``default`` module.

Save the file, then let's create our first migration.

.. code-block:: bash

  $ npx gel migration create
  did you create object type 'default::BlogPost'? [y,n,l,c,b,s,q,?]
  > y
  Created ./dbschema/migrations/00001.edgeql

The ``dbschema/migrations`` directory now contains a migration file called
``00001.edgeql``. Currently though, we haven't applied this migration against
our database. Let's do that.

.. code-block:: bash

  $ npx gel migrate
  Applied m1fee6oypqpjrreleos5hmivgfqg6zfkgbrowx7sw5jvnicm73hqdq (00001.edgeql)

Our database now has a schema consisting of the ``BlogPost`` type. We can
create some sample data from the REPL. Run the |gelcmd| command to re-open
the REPL.

.. code-block:: bash

  $ gel
  Gel x.x (repl x.x)
  Type \help for help, \quit to quit.
  gel>


Then execute the following ``insert`` statements.

.. code-block:: edgeql-repl

  gel> insert BlogPost {
  ....   title := "This one weird trick makes using databases fun",
  ....   content := "Use Gel"
  .... };
  {default::BlogPost {id: 7f301d02-c780-11ec-8a1a-a34776e884a0}}
  gel> insert BlogPost {
  ....   title := "How to build a blog with Gel and Next.js",
  ....   content := "Let's start by scaffolding our app..."
  .... };
  {default::BlogPost {id: 88c800e6-c780-11ec-8a1a-b3a3020189dd}}


Loading posts with React Server Components
------------------------------------------

Now that we have a couple posts in the database, let's load them into our
Next.js app.
To do that, we'll need the ``gel`` client library. Let's install that from
NPM:

.. code-block:: bash

  $ npm install gel
  # or 'yarn add gel' or 'pnpm add gel' or 'bun add gel'

Then go to the ``app/page.tsx`` file to replace the static data with
the blogposts fetched from the database.

To fetch these from the homepage, we'll create a Gel client and use the
``.query()`` method to fetch all the posts in the database with a
``select`` statement.

.. code-block:: tsx-diff
  :caption: app/page.tsx

    import Link from 'next/link'
  + import { createClient } from 'gel';

    type Post = {
      id: string
      title: string
      content: string
    }
  + const client = createClient();

    export default async function Home() {
  -   const posts: Post[] = [
  -     {
  -       id: 'post1',
  -       title: 'This one weird trick makes using databases fun',
  -       content: 'Use Gel',
  -     },
  -     {
  -       id: 'post2',
  -       title: 'How to build a blog with Gel and Next.js',
  -       content: "Start by scaffolding our app with `create-next-app`.",
  -     },
  -   ]
  +   const posts = await client.query<Post>(`\
  +    select BlogPost {
  +      id,
  +      title,
  +      content
  +   };`)

      return (
        <div className="container mx-auto p-4 bg-black text-white">
          <h1 className="text-3xl font-bold mb-4">Posts</h1>
          <ul>
            {posts.map((post) => (
              <li
                key={post.id}
                className="mb-4"
              >
                <Link
                  href={`/post/${post.id}`}
                  className="text-blue-500"
                >
                  {post.title}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )
    }

When you refresh the page, you should see the blog posts.

Generating the query builder
----------------------------

Since we're using TypeScript, it makes sense to use Gel's powerful query
builder. This provides a schema-aware client API that makes writing strongly
typed EdgeQL queries easy and painless. The result type of our queries will be
automatically inferred, so we won't need to manually type something like
``type Post = { id: string; ... }``.

First, install the generator to your project.

.. code-block:: bash

  $ npm install --save-dev @gel/generate
  $ # or yarn add --dev @gel/generate
  $ # or pnpm add --dev @gel/generate
  $ # or bun add --dev @gel/generate

Then generate the query builder with the following command.

.. code-block:: bash

  $ npx @gel/generate edgeql-js
  Generating query builder...
  Detected tsconfig.json, generating TypeScript files.
     To override this, use the --target flag.
     Run `npx @gel/generate --help` for full options.
  Introspecting database schema...
  Writing files to ./dbschema/edgeql-js
  Generation complete! 🤘
  Checking the generated query builder into version control
  is not recommended. Would you like to update .gitignore to ignore
  the query builder directory? The following line will be added:

     dbschema/edgeql-js

  [y/n] (leave blank for "y")
  > y


This command introspected the schema of our database and generated some code
in the ``dbschema/edgeql-js`` directory. It also asked us if we wanted to add
the generated code to our ``.gitignore``; typically it's not good practice to
include generated files in version control.

Back in ``app/page.tsx``, let's update our code to use the query builder
instead.

.. code-block:: typescript-diff
  :caption: app/page.tsx

    import Link from 'next/link'
    import { createClient } from 'gel';
  + import e from '@/dbschema/edgeql-js';

  - type Post = {
  -   id: string
  -   title: string
  -   content: string
  - }
    const client = createClient();

    export default async function Home() {
  -   const posts = await client.query(`\
  -    select BlogPost {
  -      id,
  -      title,
  -      content
  -   };`)
  +   const selectPosts = e.select(e.BlogPost, () => ({
  +     id: true,
  +     title: true,
  +     content: true,
  +   }));
  +   const posts = await selectPosts.run(client);

      return (
        <div className="container mx-auto p-4 bg-black text-white">
          <h1 className="text-3xl font-bold mb-4">Posts</h1>
          <ul>
            {posts.map((post) => (
              <li
                key={post.id}
                className="mb-4"
              >
                <Link
                  href={`/post/${post.id}`}
                  className="text-blue-500"
                >
                  {post.title}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )
    }

Instead of writing our query as a plain string, we're now using the query
builder to declare our query in a code-first way. As you can see, we import the
query builder as a single default import ``e`` from the ``dbschema/edgeql-js``
directory.

Now, when we update our ``selectPosts`` query, the type of our dynamically
loaded ``posts`` variable will update automatically — no need to keep
our type definitions in sync with our API logic!

Rendering blog posts
--------------------

Our homepage renders a list of links to each of our blog posts, but we haven't
implemented the page that actually displays the posts. Let's create a new page
at ``app/post/[id]/page.tsx``. This is a
`dynamic route <https://nextjs.org/docs/app/building-your-application/
routing/dynamic-routes>`_ that
includes an ``id`` URL parameter. We'll use this parameter to fetch the
appropriate post from the database.

Add the following code in ``app/post/[id]/page.tsx``:

.. code-block:: tsx
  :caption: app/post/[id]/page.tsx

  import { createClient } from 'gel'
  import e from '@/dbschema/edgeql-js'
  import Link from 'next/link'

  const client = createClient()

  export default async function Post({ params }: { params: { id: string } }) {
    const post = await e
      .select(e.BlogPost, (post) => ({
        id: true,
        title: true,
        content: true,
        filter_single: e.op(post.id, '=', e.uuid(params.id)),
      }))
      .run(client)

    if (!post) {
      return <div>Post not found</div>
    }

    return (
      <div className="container mx-auto p-4 bg-black text-white">
        <nav>
          <Link
            href="/"
            className="text-blue-500 mb-4 block"
            replace
          >
            Back to list
          </Link>
        </nav>
        <h1 className="text-3xl font-bold mb-4">{post.title}</h1>
        <p>{post.content}</p>
      </div>
    )
  }

We are again using a Server Component to fetch the post from the database.
This time, we're using the ``filter_single`` method to filter the
``BlogPost`` type by its ``id``. We're also using the ``uuid`` function
from the query builder to convert the ``id`` parameter to a UUID.

Now, click on one of the blog post links on the homepage. This should bring
you to ``/post/<uuid>``.

Deploying to Vercel
-------------------

You can deploy a Gel instance on the Gel Cloud or
on your preferred cloud provider. We'll cover both options here.

With Gel Cloud
==============

**#1 Deploy Gel**

First, sign up for an account at
`cloud.geldata.com <https://cloud.geldata.com>`_ and create a new instance.
Create and make note of a secret key for your Gel Cloud instance. You
can create a new secret key from the "Secret Keys" tab in the Gel Cloud
console. We'll need this later to connect to the database from Vercel.

Run the following command to migrate the project to the Gel Cloud:

.. code-block:: bash

  $ npx gel migrate -I <org>/<instance-name>

.. note::

  Alternatively, if you want to restore your data from a local instance to
  the cloud, you can use the :gelcmd:`dump` and :gelcmd:`restore` commands.

.. code-block:: bash

  $ npx gel dump <your-dump.dump>
  $ npx gel restore -I <org>/<instance-name> <your-dump.dump>

The migrations and schema will be automatically applied to the
cloud instance.

**#2 Set up a `prebuild` script**

Add the following ``prebuild`` script to your ``package.json``. When Vercel
initializes the build, it will trigger this script which will generate the
query builder. The ``npx @gel/generate edgeql-js`` command will read the
value of the :gelenv:`SECRET_KEY` and :gelenv:`INSTANCE` variables,
connect to the database, and generate the query builder before Vercel
starts building the project.

.. code-block:: javascript-diff

    // package.json
    "scripts": {
      "dev": "next dev",
      "build": "next build",
      "start": "next start",
      "lint": "next lint",
  +   "prebuild": "npx @gel/generate edgeql-js"
    },

**#3 Deploy to Vercel**

Push your project to GitHub or some other Git remote repository. Then deploy
this app to Vercel with the button below.


.. XXX -- update URL
.. lint-off

.. image:: https://vercel.com/button
  :width: 150px
  :target: https://vercel.com/new/git/external?repository-url=https://github.com/geldata/gel-examples/tree/main/nextjs-blog&project-name=nextjs-edgedb-blog&repository-name=nextjs-edgedb-blog&env=EDGEDB_DSN,EDGEDB_CLIENT_TLS_SECURITY

.. lint-on

In "Configure Project," expand "Environment Variables" to add two variables:

- :gelenv:`INSTANCE` containing your Gel Cloud instance name (in
  ``<org>/<instance-name>`` format)
- :gelenv:`SECRET_KEY` containing the secret key you created and noted
  previously.

**#4 View the application**

Once deployment has completed, view the application at the deployment URL
supplied by Vercel.

With other cloud providers
===========================

**#1 Deploy Gel**

Check out the following guides for deploying Gel to your preferred cloud
provider:

- :ref:`AWS <ref_guide_deployment_aws_aurora_ecs>`
- :ref:`Google Cloud <ref_guide_deployment_gcp>`
- :ref:`Azure <ref_guide_deployment_azure_flexibleserver>`
- :ref:`DigitalOcean <ref_guide_deployment_digitalocean>`
- :ref:`Fly.io <ref_guide_deployment_fly_io>`
- :ref:`Docker <ref_guide_deployment_docker>`
  (cloud-agnostic)

**#2 Find your instance's DSN**

The DSN is also known as a connection string. It will have the format
:geluri:`username:password@hostname:port`. The exact instructions for this
depend on which cloud you are deploying to.

**#3 Apply migrations**

Use the DSN to apply migrations against your remote instance.

.. code-block:: bash

  $ npx gel migrate --dsn <your-instance-dsn> --tls-security insecure

.. note::

  You have to disable TLS checks with ``--tls-security insecure``. All Gel
  instances use TLS by default, but configuring it is out of scope of this
  project.

Once you've applied the migrations, consider creating some sample data in your
database. Open a REPL and ``insert`` some blog posts:

.. code-block:: bash

  $ npx gel --dsn <your-instance-dsn> --tls-security insecure
  Gel x.x (repl x.x)
  Type \help for help, \quit to quit.
  gel> insert BlogPost { title := "Test post" };
  {default::BlogPost {id: c00f2c9a-cbf5-11ec-8ecb-4f8e702e5789}}


**#4 Set up a `prebuild` script**

Add the following ``prebuild`` script to your ``package.json``. When Vercel
initializes the build, it will trigger this script which will generate the
query builder. The ``npx @gel/generate edgeql-js`` command will read the
value of the :gelenv:`DSN` variable, connect to the database, and generate
the query builder before Vercel starts building the project.

.. code-block:: javascript-diff

    // package.json
    "scripts": {
      "dev": "next dev",
      "build": "next build",
      "start": "next start",
      "lint": "next lint",
  +   "prebuild": "npx @gel/generate edgeql-js"
    },

**#5 Deploy to Vercel**

Deploy this app to Vercel with the button below.

.. lint-off

.. image:: https://vercel.com/button
  :width: 150px
  :target: https://vercel.com/new/git/external?repository-url=https://github.com/geldata/gel-examples/tree/main/nextjs-blog&project-name=nextjs-edgedb-blog&repository-name=nextjs-edgedb-blog&env=EDGEDB_DSN,EDGEDB_CLIENT_TLS_SECURITY

.. lint-on

When prompted:

- Set :gelenv:`DSN` to your database's DSN
- Set :gelenv:`CLIENT_TLS_SECURITY` to ``insecure``. This will disable
  Gel's default TLS checks; configuring TLS is beyond the scope of this
  tutorial.

.. XXX -- update URL

.. image::
    https://www.geldata.com/docs/tutorials/nextjs/env.png
    :alt: Setting environment variables in Vercel
    :width: 100%


**#6 View the application**

Once deployment has completed, view the application at the deployment URL
supplied by Vercel.

Wrapping up
-----------

This tutorial demonstrates how to work with Gel in a
Next.js app, using the App Router. We've created a simple blog application
that loads posts from a database and displays them on the homepage.
We've also created a dynamic route that fetches a single post from the
database and displays it on a separate page.

The next step is to add a ``/newpost`` page with a form for writing new blog
posts and saving them into Gel. That's left as an exercise for the reader.

To see the final code for this tutorial, refer to
`github.com/geldata/gel-examples/tree/main/nextjs-blog
<https://github.com/geldata/gel-examples/tree/main/
nextjs-blog-app-router>`_.
