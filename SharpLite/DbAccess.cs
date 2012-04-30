using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using PetaPoco;

namespace SharpLite
{
    class DbAccess
    {
        private static Database m_instance = null;

        public static Database GetInstance()
        {
            if (m_instance == null)
            {
                m_instance = new Database("SharpLite.Properties.Settings.SQLite");
            }
            return m_instance;
        }
    }
}
